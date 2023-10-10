import openai
from flask import Flask, request, jsonify
from mongo_client import chat_finder, chat_exist, new_chat
from api_key import key

app = Flask(__name__)

openai.api_key = key


@app.route("/add", methods=['POST'])
def addition():
    user_input = request.json
    sys_prompt = user_input["prompt"]
    user_prompt = user_input["user_id"]

    conversation_history = []
    chat_document = chat_finder(user_prompt)

    if chat_document is not None:
        response1 = chat_exist(chat_document, sys_prompt)
        return jsonify({"response": response1})
    else:
        response1, chat_id = new_chat(user_prompt, sys_prompt, conversation_history)
        return jsonify({"response": response1, "chat_id": chat_id})


if __name__ == '__main__':
    app.run(port=5080)
