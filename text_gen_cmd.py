import streamlit as st
import speech_recognition as sr
import threading

# Initialize the recognizer
recognizer = sr.Recognizer()
audio = None
is_recording = False

def record_audio():
    global audio, is_recording
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        audio = recognizer.listen(source)
        is_recording = False

def recognize_speech():
    global audio
    try:
        text = recognizer.recognize_google(audio)
        st.session_state.question = text
    except sr.UnknownValueError:
        st.session_state.question = "Sorry, I could not understand the audio."
    except sr.RequestError:
        st.session_state.question = "Could not request results from Google Speech Recognition service."

# Streamlit app
st.title("Voice Input Example")

col1, col2 = st.columns(2)

# Define state to manage button visibility
if "show_stop" not in st.session_state:
    st.session_state.show_stop = False

with col1:
    if st.session_state.show_stop:
        if st.button("Stop"):
            if is_recording:
                is_recording = False
                recognize_speech()
                st.session_state.show_stop = False
            else:
                st.warning("No ongoing recording to stop.")
    else:
        if st.button("Say"):
            if not is_recording:
                is_recording = True
                st.session_state.show_stop = True
                # Start recording in a separate thread to avoid blocking the main thread
                threading.Thread(target=record_audio).start()
            else:
                st.warning("Already recording. Please wait until it stops.")

    if "question" in st.session_state:
        st.text_area("Question:", st.session_state.question, height=300)
