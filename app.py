from flask import Flask, request, jsonify, render_template
# import your_nlp_model  # Replace this with your actual NLP model import
from yt_link import transcript
from bot import QNA
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    print(data)
    user_text = data['prompt']
    data = transcript(user_text)
    # bot(bot)
    # Get response from your NLP model
    # nlp_response = your_nlp_model.get_response(user_text)  # Replace this with your actual model call

    return jsonify({
        'response': 'hello'
    })

if __name__ == '__main__':
    app.run(debug=True)
