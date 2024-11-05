from flask import Flask, send_from_directory

def create_app(test_config=None):
    app = Flask(__name__, static_folder='./static', static_url_path='/')

    @app.after_request
    def apply_no_sniff(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    @app.route('/')
    def send_index():
        return app.send_static_file('index.html')

    return app 