from flask import Flask, jsonify, request, Request
import json, jwt
from .database import accounts, chats

def get_session_username(request: Request):
    token = request.cookies.get('AUTH_TOKEN', default=None)
    decoded = jwt.decode(token, "SECRET_KET", algorithms=["HS256"])
    username = decoded.get("uid")
    return username


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
            data = request.get_json()
            message = data.get('message')
        
            if not message:  # Handle missing or invalid messages
                return jsonify({"error": "Message is required"}), 400
        
            # Add the message to the chat history
            success = chats.postChat(message, "Guest")
            if success:
                return jsonify({"success": True}), 201
            else:
                return jsonify({"error": "Failed to add chat"}), 500
        except Exception as e:
            return jsonify({"error": "Failed to send message"}), 500

    return app