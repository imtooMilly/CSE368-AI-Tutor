from flask import Flask, jsonify, request, Request
import json, jwt, os
from .database import accounts, chats
from .quiz_generation_with_interactivity import interactive_quiz, conversational_agent
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = './uploads' 
# ALLOWED_EXTENSIONS = {'pdf', 'txt', 'jpg', 'png', 'jpeg'} 

def get_session_username(request: Request):
    token = request.cookies.get('AUTH_TOKEN', default=None)
    decoded = jwt.decode(token, "SECRET_KET", algorithms=["HS256"])
    username = decoded.get("uid")
    return username


def create_app(test_config=None):
    app = Flask(__name__, static_folder='./static', static_url_path='/')

    UPLOAD_FOLDER = 'uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

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
            # Get the chat message from the form
            message = request.form.get('message')
            if not message:
                return jsonify({"error": "Message is required"}), 400

            # Check if the request contains a file
            uploaded_file = request.files.get('file')
            file_path = None

            if uploaded_file:
                # Ensure the file has a valid filename and is allowed
                filename = uploaded_file.filename
                if filename != '':
                    # Secure the filename and save the file in the uploads directory
                    filename = secure_filename(filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    uploaded_file.save(file_path)
                else:
                    return jsonify({"error": "Invalid file type or no file selected"}), 400

            # Add the message to the chat history (you can add the file path if necessary)
            success = chats.postChat(message, "Guest")

            # Process the message and file path with your interactive quiz function
            response = interactive_quiz(message, file_path)

            # Optionally, post the response to the chat history
            chats.postChat(response, "AKINATOR")

            # Return a success response
            if success:
                return jsonify({"success": True}), 201
            else:
                return jsonify({"error": "Failed to add chat"}), 500

        except Exception as e:
            return jsonify({"error": f"Failed to send message: {str(e)}"}), 500

    return app