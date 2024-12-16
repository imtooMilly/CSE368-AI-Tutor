from flask import Flask
import json, jsonify
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
        history = chats.getChatHistory()
        return jsonify(history), 200

    return app