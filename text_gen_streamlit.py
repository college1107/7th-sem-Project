import pyttsx3

def speak_text(text, voice_name=None):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # List available voices
    voices = engine.getProperty('voices')
    
    # Set the voice
    if voice_name:
        for voice in voices:
            if voice_name in voice.name:
                engine.setProperty('voice', voice.id)
                break
    else:
        # Default to the first available voice if no custom voice is specified
        engine.setProperty('voice', voices[0].id)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

# Example usage:
speak_text("Hello, this is a test.", "woman")
