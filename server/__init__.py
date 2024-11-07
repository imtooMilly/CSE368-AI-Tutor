from flask import Flask, send_from_directory, request, jsonify, Response
import os
from http import client
import json

from database import accounts, session

def create_app(test_config=None):
    # Specify client/build as the static folder
    app = Flask(__name__, static_folder='../client/build', static_url_path='/')

    @app.after_request
    def apply_no_sniff(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    # Serve the React app's index.html for the root and unmatched routes
    @app.route('/')
    @app.route('/<path:path>')
    def serve_react_app(path=""):
        # Check if the requested path exists in the static folder
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            # Serve index.html for unmatched routes
            return send_from_directory(app.static_folder, 'index.html')
        
    @app.route('/login', methods=['POST'])
    def login():
        if request.authorization is None:
            return jsonify({'error': "Missing Authorization header"}), client.BAD_REQUEST

        if request.authorization.type != 'basic':
            return jsonify(
                {'error': f"Unsupported Authorization type: {request.authorization.type}"}), client.BAD_REQUEST

        email = request.authorization.get('username', '')
        password = request.authorization.get('password', '')

        account = accounts.check_credentials(email, password)
        if account is None:
            return jsonify({'error': "Invalid email and/or password"}), client.NOT_FOUND

        sess = session.createSession(account.get('username', ''))

        response = Response(status=client.OK)
        # set secure=True if we move over to HTTPS
        response.set_cookie('AUTH_TOKEN', sess['token'], expires=sess['expires'], httponly=True, samesite='Lax')

        response.set_data(json.dumps({'username': account['username']}))
        return response
    
    @app.route('/logout', methods=['POST'])
    def logout():
        token = request.cookies.get('AUTH_TOKEN', None)
        if token is not None:
            session.delete_session(token)
        response = Response(status=client.NO_CONTENT)
        response.set_cookie('AUTH_TOKEN', '', expires=0, httponly=True, samesite='Lax')
        return response

    return app

