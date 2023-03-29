import openai
import whisper
import pickle
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv('API_KEY')


API_KEY = os.getenv('API_KEY')
openai.api_key = API_KEY
model = whisper.load_model("base")


def make_note(command, fname, is_transcribed):
    if is_transcribed is False:
        result = model.transcribe(f'static/upload/{fname[14:]}')
        with open('memory/transcription.tkl', 'wb') as f:
            pickle.dump(result, f)
    else:
        with open('memory/transcription.tkl', 'rb') as f:
            result = pickle.load(f)

    messages=[
            {"role": "system", "content": "You are a physician. Answer to the highest degree of medical accuracy. Use medical jargon where appropriate. Fulfill the user's command using the transcription. Use bullet points where appropriate. Use full sentences where appropriate. Do not make up information. If you don't know something, say you don't know."},
            {"role": "user", "content": f'Command: Create {command}\n\nTranscription: {result["text"]}'},
        ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # saving SOAP note
    msg_path = 'memory/msg.tkl'
    if os.path.isfile(msg_path):
        with open(msg_path, 'rb') as f:
            messages = pickle.load(f)
            messages.append({"role": "system", "content": response['choices'][0]['message']['content']})
    else:
        messages = [{"role": "system", "content": response['choices'][0]['message']['content']}]

    with open(msg_path, 'wb') as f:
        pickle.dump(messages, f)

    return response['choices'][0]['message']['content'].strip().replace('\n', '<br>')
