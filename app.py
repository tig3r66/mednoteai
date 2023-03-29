from flask import Flask, render_template, request
from convo_sum_buff_mem import main
from process_data import make_note, make_questions, make_mcqs, make_paper
import os
import glob




def chatbot_response(msg):
    if msg is None:
       return ""
    elif len(msg) > 10000:
        return "There are too many characters in your message (max: 10000). Please try again."
    return main(msg)


app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = 'templates'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = str(request.args.get('msg'))
    if userText == '!process':
        files = glob.glob('static/upload/*')
        if len(files) == 0:
            return "No file uploaded. Please upload a video or PDF first."
        latest_file = max(files, key=os.path.getctime)
        transcribed = False
        if os.path.isfile('memory/notes.tkl'):
            transcribed = True
        return make_note(latest_file.strip('static/upload/'), transcribed)
    elif userText == '!paper':
        files = glob.glob('static/upload/*')
        if len(files) == 0:
            return "No file uploaded. Please upload a video or PDF first."
        latest_file = max(files, key=os.path.getctime)
        transcribed = False
        if os.path.isfile('memory/notes.tkl'):
            transcribed = True
        return make_paper(latest_file.strip('static/upload/'), transcribed)
    elif userText == 'None':
        return ''
    elif '!q' in userText:
        files = glob.glob('memory/notes.tkl')
        if len(files) == 0:
            return "No file uploaded. Please upload a video or PDF first."
        try:
            return make_questions('memory/notes.tkl', userText.strip().split()[1]).strip()
        except:
            return "I can't process this request. Please try again."
    elif '!mcq' in userText:
        files = glob.glob('memory/notes.tkl')
        if len(files) == 0:
            return "No file uploaded. Please upload a video or PDF first."
        try:
            return make_mcqs('memory/notes.tkl', userText.strip().split()[1]).strip()
        except:
            return "I can't process this request. Please try again."
    elif userText[0] == '!':
        return "I can't process this request. Please try again."
    return chatbot_response(userText)


@app.before_first_request
def delete_msg():
    files = glob.glob('memory/chunks/*')
    if len(files) != 0:
        for f in files:
            os.remove(f)
    files = glob.glob('memory/*[!chunks]')
    if len(files) != 0:
        for f in files:
            os.remove(f)
    files = glob.glob('static/upload/*')
    if len(files) != 0:
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
    app.run(debug=True)
