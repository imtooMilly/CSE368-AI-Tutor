from flask import Flask, jsonify
import requests
import json
from .database import accounts, chats


def create_app(test_config=None):
    app = Flask(__name__, static_folder='./static', static_url_path='/')

    # Serve React's index.html for the base route
    @app.route('/')
    def send_index():
        return app.send_static_file('index.html')

    # Serve React's index.html for /login, /register, and /chat
    @app.route('/login')
    def login():
        return app.send_static_file('index.html')

    @app.route('/register')
    def register():
        return app.send_static_file('index.html')

    @app.route('/chat')
    def chat():
        return app.send_static_file('index.html')
    
    @app.route('/chat-history', methods=['GET'])
    def pull_history():
        try:
            # Assuming chatHistory is a list of messages
            chat_history = chats.getChatHistory()  # Fetch history from the database
            return jsonify(chat_history), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "Failed to fetch chat history"}), 500

    @app.route('/send-chat', methods=['POST'])
    def send_chat():
        try:
            data = requests.get_json()
            message = data.get('message')
            # Add the message to the chat history
            add_message_to_history(message)
            return jsonify({"success": True}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "Failed to send message"}), 500

    return app