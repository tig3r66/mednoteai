import openai
import numpy as np
import pandas as pd
import pickle
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv('API_KEY')


def answer_query_with_context(
    query: str,
    msg_path: str,
    show_prompt: bool = False,
) -> str:

    prompt = query
    if show_prompt:
        print(prompt)

    # chat memory ====
    instructions = {"role": "system", "content": "You are a specialist physician. Answer to the highest degree of medical accuracy. Use medical jargon where appropriate. Write 'This is outside the scope of my functionality.' if the query does not relate to medicine or a previous response. Do not make up information. If you don't know something, say you don't know."}
    if os.path.isfile(msg_path):
        with open(msg_path, 'rb') as f:
            messages = pickle.load(f)
    else:
        messages = [instructions]

    messages.append({"role": "user", "content": prompt})
    # getting response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        top_p=1,)['choices'][0]['message']['content']

    messages[-1] = {"role": "user", "content": query}
    messages.append({"role": "system", "content": response})

    while len(messages) > 8:
        messages.pop(0)

    # saving conversation
    with open(msg_path, 'wb') as f:
        pickle.dump(messages, f)

    return response


def main(prompt):
    msg_path = 'memory/msg.tkl'
    return answer_query_with_context(prompt, msg_path).replace('\n', '<br>')
