import openai
from flask import Flask, request, jsonify
from functions import chat_finder, chat_exist, new_chat, generate_id
from config import key

app = Flask(__name__)

openai.api_key = key


@app.route("/add", methods=['POST'])
def addition():
    object_id = generate_id()
    user_input = request.json
    sys_prompt = user_input["prompt"]
    user_prompt = user_input["user_id"]
    cont_convo = user_input["same_conversation"]

    conversation_history = []
    chat_document = chat_finder(user_prompt)

    if chat_document is None:
        session_id = generate_id()  # Generate a new session ID for new conversations
        response1, chat_id = new_chat(object_id, user_prompt, sys_prompt, conversation_history, session_id)
        return jsonify({"response": response1, "chat_id": chat_id})
    else:
        if cont_convo.lower() == "yes":
            # No new session ID is generated for continuing old conversations
            response1 = chat_exist(chat_document, sys_prompt)
            return jsonify({"response": response1})
        else:
            session_id = generate_id()  # Generate a new session ID for new conversations
            response1 = chat_exist(chat_document, sys_prompt, session_id)  # Pass session_id here
            return jsonify({"response": response1})


if __name__ == '__main__':
    app.run(port=5080)
