from flask import Flask, request, jsonify, render_template
# import your_nlp_model  # Replace this with your actual NLP model import

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data['prompt']

    # Get response from your NLP model
    # nlp_response = your_nlp_model.get_response(user_text)  # Replace this with your actual model call

    return jsonify({
        'response': 'hello'
    })

if __name__ == '__main__':
    app.run(debug=True)
