
# Chatbot Application

A simple chatbot application built with Python and the OpenAI GPT-3.5 model, powered by a Flask API and MongoDB.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [License](#license)

## Overview

This project is a chatbot application that allows users to have text-based conversations with a chatbot powered by OpenAI's GPT-3.5 model. The application is designed to manage and track conversations in a MongoDB database, enabling both new and ongoing dialogues.

## Features

- Create new conversations or continue existing ones with the chatbot.
- Store conversation history in a MongoDB database.
- Generate unique chat and session IDs.
- Easy-to-use API for interacting with the chatbot.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Adinyk03/Chatbot_openai.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the project by editing the `config.py` file. Set your MongoDB connection string and OpenAI API key.

## Usage

1. Start the Flask server:

   ```bash
   python main.py
   ```

2. Make POST requests to the `/add` endpoint to interact with the chatbot. Provide the following JSON data in the request body:

   ```json
   {
     "prompt": "Your prompt here",
     "user_id": "User identifier",
     "same_conversation": "yes"
   }
   ```

3. The API will respond with the chatbot's reply and a unique chat ID.

## API Endpoints

- `POST /add`: Add a new conversation or continue an existing one with the chatbot.

### Example Request

```json
{
  "prompt": "Tell me a joke",
  "user_id": "12345",
  "same_conversation": "yes"
}
```

### Example Response

```json
{
  "response": "Why did the chicken cross the road? To get to the other side!",
  "chat_id": "chat123456"
}
```

## File Structure

The project's file structure is as follows:

- `main.py`: The main application file.
- `functions.py`: Contains functions for managing conversations and interacting with the chatbot.
- `config.py`: Configuration file for database connection and API key.
- `alphanum.py`: Utility to generate unique IDs.
- `requirements.txt`: List of project dependencies.

## Configuration

- Configure the MongoDB connection string in the `config.py` file under `client_var`.
- Set your OpenAI API key in the `config.py` file under `key`.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

