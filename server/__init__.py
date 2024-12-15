from flask import Flask, send_from_directory
import os

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

    return app

