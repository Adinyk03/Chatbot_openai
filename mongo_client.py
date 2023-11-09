import openai
from pymongo import MongoClient
from config import collection_var, client_var, db_var
from alphanum import generate


# generates 16 digit alphanumeric code
def generate_id():
    return generate(16)


# MongoDB client Initialization
def chat_finder(user_prompt):
    client = MongoClient(client_var)
    db = client[db_var]
    collection = db[collection_var]
    x = collection.find_one({"User Prompt": user_prompt})
    return x


def chat_update(chat_id, chat_document):
    client = MongoClient(client_var)
    db = client[db_var]
    collection = db[collection_var]
    y = collection.update_one({"_id": chat_id}, {"$set": chat_document}, upsert=True)
    return y


def chat_response(prompt, conversation_hist=None, session_id=None):
    # Define a system message
    if conversation_hist is None:
        conversation_hist = []
    system_message = {"role": "system", "content": "You can give me the answers"}
    sess_id = None

    if session_id is not None:
        sess_id = {"role": "assistant", "content": f"session id - {session_id}"}
        messages = conversation_hist + [system_message, sess_id, {"role": "user", "content": f"{prompt}"}]
    else:
        # Combine conversation history with the user's prompt
        messages = conversation_hist + [system_message, {"role": "user", "content": f"{prompt}"}]

    # Generate a response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
    )

    if session_id and sess_id is not None:
        conversation_hist.append(sess_id)

    user_message = {"role": "user", "content": prompt}
    assistant_message = {"role": "assistant", "content": response.choices[0].message.content}

    # Append messages to the conversation history
    conversation_hist.append(user_message)
    conversation_hist.append(assistant_message)

    return response.choices[0].message.content, conversation_hist


def new_chat(object_id, user_prompt, sys_prompt, conversation_history, session_id):
    response1, conversation_history = chat_response(sys_prompt, conversation_history)
    chat_message = {
        "_id": object_id,
        "User Prompt": user_prompt,
        "assistant response": response1,
        "first session id": session_id,
        "conversation history": conversation_history
    }
    chat_update(object_id, chat_message)
    return response1, str(object_id)


def chat_exist(chat_document, sys_prompt, session_id=None):
    chat_id = chat_document["_id"]
    conversation_history = chat_document.get("conversation_history", [])
    response1, conversation_history = chat_response(sys_prompt, conversation_history, session_id)
    chat_document["conversation_history"] = conversation_history
    chat_update(chat_id, chat_document)
    return response1
