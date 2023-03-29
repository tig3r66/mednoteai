from flask import Flask, render_template, request
from convo_sum_buff_mem import main
from audio_process import make_note
import os
import glob


def process_msg(result):
  if result[0].strip() == "This is outside the scope of my functionality." or \
    "no medical question" in result[0].strip() or \
    "neurosurgery or vestibular schwannoma" in result[0].strip():
     return result[0].strip()
  return result[0].replace("'", "").replace('\n', '<br>')


def chatbot_response(msg):
    if msg is None:
       return ""
    elif len(msg) > 10000:
        return "There are too many characters in your message (max: 10000). Please try again."
    return process_msg(main(msg))


app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = 'templates'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = str(request.args.get('msg'))
    if userText[0] == '!':
        files = glob.glob('static/upload/*')
        if len(files) == 0:
            return "No file uploaded. Please upload audio first."
        latest_file = max(files, key=os.path.getctime)
        transcribed = False
        if os.path.isfile('memory/transcription.tkl'):
            transcribed = True
        return make_note(userText[1:], latest_file, transcribed)
    if userText == 'None':
        return ''
    return chatbot_response(userText)


@app.before_first_request
def delete_msg():
    files = glob.glob('memory/*')
    for f in files:
        os.remove(f)
    files = glob.glob('static/upload/*')
    for f in files:
        os.remove(f)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join('static', 'upload', filename))
        return 'File uploaded successfully'
    return 'No file uploaded'


if __name__ == "__main__":
    app.run()
