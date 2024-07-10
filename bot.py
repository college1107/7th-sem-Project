from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re
import spacy
import requests
from bs4 import BeautifulSoup
def Title(link):
    res = requests.get(link)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    video_title = soup.find('meta', property='og:title')['content']
    return video_title

def transcript(link):
    # link = 'https://www.youtube.com/watch?v=FhgQXUR5OZE'
    try:
        video_id = re.findall(r"v=([A-Za-z0-9_-]*)", link)
        # print(video_id)
        if video_id:
            video_id = video_id[0]
            title = f"Title or Main topic or title of the video is {Title(link)}"
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            strings = [entry["text"] for entry in transcript]
            strings.insert(0, title)
            # print(strings)
            return " ".join(strings)
        else:
            print("No video ID found in the link.")
    except Exception as e:
        print(f"An error occurred: {e}")


def PreProcess(text):
    nlp_spacy = spacy.load("en_core_web_lg")
    doc = nlp_spacy(text)
    tokens = [token.text for token in doc if not token.is_punct]
    return " ".join(tokens)


def QNA(question, context):
    model_name = "deepset/roberta-base-squad2"
    nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)
    QA_input = {"question": f"{question}", "context": None}
    QA_input["context"] = PreProcess(context)
    res = nlp(QA_input)
    print(res)
    return str(res["answer"])


# transcript()
