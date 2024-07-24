import google.generativeai as genai
import signal
import sys

api_key = "api"  #add your API key
genai.configure(api_key=api_key)

def generate_extended_answer(prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        max_tokens = 3000
        temperature = 0.7
        response = model.generate_content([prompt])
        
        return response.text
    except Exception as e:
        return "Error generating answer."

def signal_handler(sig, frame):
    sys.exit(0)  

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        try:
            prompt = input("Enter your question: ")
            if prompt:
                answer = generate_extended_answer(prompt)
                if answer:
                    print(f"Q: {prompt}")
                    print(f"A: {answer}")
                else:
                    print("Error generating answer.")
            else:
                print("No question entered.")
        except KeyboardInterrupt:
            break 

if __name__ == "__main__":
    main()
