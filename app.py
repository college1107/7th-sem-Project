from flask import Flask, render_template, request, jsonify
import bot as b
app = Flask(__name__)

# Simulated function to check if a YouTube link is valid
def is_valid_youtube_link(link):
    return "youtube.com" in link or "youtu.be" in link

@app.route('/')
def index():
    return render_template('index.html')
yt_link=str()
@app.route('/validate_link', methods=['POST'])
def validate_link():
    global yt_link
    data = request.get_json()
    yt_link = data.get('yt_link', '')
    is_valid = is_valid_youtube_link(yt_link)
    return jsonify({'is_valid': is_valid})

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get('question', '')
    link_data = b.transcript(yt_link)
    res = b.QNA(question,link_data)
    answer = res
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
