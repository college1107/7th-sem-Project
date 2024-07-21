import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from bs4 import BeautifulSoup
from transformers import pipeline
import warnings
import spacy
import requests
import openai

warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# OpenAI API 
openai.api_key = "sk-proj-XmmWBu7Xle2RiNjmkSYfT3BlbkFJmOtJLv4FfSsD4QXb3RPy"

def Title(link):
    try:
        res = requests.get(link)
        html_content = res.text
        soup = BeautifulSoup(html_content, 'html.parser')
        video_title = soup.find('meta', property='og:title')['content']
        return video_title
    except Exception as e:
        return f"Error fetching title: {e}"

def PreProcess(text, link):
    nlp_spacy = spacy.load("en_core_web_lg")
    title = f"Title or main topic of the video is {Title(link)}"
    doc = nlp_spacy(text)
    tokens = [token.text for token in doc if not token.is_punct and not token.is_stop]
    tokens.append(title)
    return " ".join(tokens)

def QNA(question, context):
    model_name = "deepset/roberta-base-squad2"
    nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)
    QA_input = {"question": question, "context": context}
    try:
        res = nlp(QA_input)
        return str(res["answer"])
    except Exception as e:
        return f"Error in QNA: {e}"

def generate_extended_answer(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error in generating extended answer: {e}"

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        return str(e)

def main():
    st.title("YouTube Transcript Q/A Chatbot")
    if 'output_placeholder' not in st.session_state:
        st.session_state.output_placeholder = ""

    link = st.text_input("Enter YouTube Link")

    transcript = ""
    if link:
        try:
            video_id = link.split("v=")[1].split("&")[0]  # Handle cases with additional parameters
            transcript = fetch_transcript(video_id)
            if transcript:
                st.success("Transcript fetched successfully!")
            else:
                st.warning("No transcript found or transcript is disabled for this video.")
        except IndexError:
            st.error("Invalid YouTube link. Please enter a valid YouTube link.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    col1, col2 = st.columns(2)

    with col1:
        question = st.text_area("Question:", height=300)

    with col2:
        output = st.text_area("Answer will be displayed here:", value=st.session_state.output_placeholder, height=300)

    with col1:
        if st.button("Process"):
            if link and transcript:
                context = PreProcess(transcript, link)
                qa_answer = QNA(question, context)
                extended_answer = generate_extended_answer(f"Extend the following answer: {qa_answer}")
                st.session_state.output_placeholder = extended_answer
                st.experimental_rerun()
            else:
                st.warning("No link is entered")

if __name__ == "__main__":
    main()
