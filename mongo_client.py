import openai
from pymongo import MongoClient


# MongoDB client Initialization
def chat_finder(user_prompt):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["chat_hist"]
    collection = db["chats"]
    x = collection.find_one({"User Prompt": user_prompt})
    return x


def chat_update(chat_id, chat_document):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["chat_hist"]
    collection = db["chats"]
    y = collection.update_one({"_id": chat_id}, {"$set": chat_document})
    return y


def chat_insert(chat_message):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["chat_hist"]
    collection = db["chats"]
    z = collection.insert_one(chat_message)
    return z


def chat_response(prompt, conversation_hist=None):
    # Define a system message
    if conversation_hist is None:
        conversation_hist = []
    system_message = {"role": "system", "content": "You can give me the answers"}

    # Combine conversation history with user's prompt
    messages = conversation_hist + [system_message, {"role": "user", "content": f"{prompt}"}]

    # Generate a response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
    )

    # Create user and assistant messages
    user_message = {"role": "user", "content": prompt}
    assistant_message = {"role": "assistant", "content": response.choices[0].message.content}

    # Append messages to the conversation history
    conversation_hist.append(user_message)
    conversation_hist.append(assistant_message)

    return response.choices[0].message.content, conversation_hist


def chat_exist(chat_document, sys_prompt):
    chat_id = chat_document["_id"]
    conversation_history = chat_document.get("conversation_history", [])
    response1, conversation_history = chat_response(sys_prompt, conversation_history)
    chat_document["conversation_history"] = conversation_history
    chat_update(chat_id, chat_document)
    return response1


def new_chat(user_prompt, sys_prompt, conversation_history):
    response1, conversation_history = chat_response(sys_prompt, conversation_history)
    chat_message = {
        "User Prompt": user_prompt,
        "assistant_response": response1,
        "conversation_history": conversation_history
    }
    result = chat_insert(chat_message)
    return response1, str(result.inserted_id)
