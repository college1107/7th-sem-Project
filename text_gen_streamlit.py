import streamlit as st
import google.generativeai as genai


api_key = "AIzaSyAyRBWQ016M7-GJ65NQ9szFk-TkPHCje_U"  #add your actual API key
genai.configure(api_key=api_key)

def generate_extended_answer(prompt, max_tokens, temperature):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([prompt])
        answer = response.text
        if max_tokens:
            answer = ' '.join(answer.split()[:max_tokens])
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"

st.set_page_config(page_title="Generative AI Chat", layout="wide")

with st.sidebar:
    st.subheader("Settings")
    max_tokens = st.number_input("Maximum Tokens", min_value=1, max_value=5000, value=3000)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)

if "history" not in st.session_state:
    st.session_state.history = []
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

st.title("Generative AI Chat")

for entry in st.session_state.history:
    st.markdown(f"**Q:** {entry['question']}")
    st.markdown(f"**A:** {entry['answer']}")

st.write("---")
form = st.form(key="chat_form")
prompt = form.text_input("Enter your question:", value=st.session_state.current_prompt)
submit_button = form.form_submit_button("Submit")

if submit_button:
    if prompt:
        answer = generate_extended_answer(prompt, max_tokens, temperature)
        st.session_state.history.append({"question": prompt, "answer": answer})
        st.session_state.current_prompt = ""
        st.experimental_rerun()
    else:
        st.write("No question entered.")
