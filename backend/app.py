from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from question_generation import generate_questions_from_file
from pymongo import MongoClient
import json

# FLASK SETUP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

# DATABASE SETUP
client = MongoClient('mongodb://localhost:27017/') #might need to change from localhost after testing
db = client['AIdb']  # Database name
chats = db['chatHistory']  # chat history
accounts = db['accounts'] # account data
files = db['files'] # file data

def getChatHistory():
    chatHistory = list(chats.find({}, {"_id": 0}))
    return chatHistory

def postChat(message, user):
    chats.insert_one(
        {
            "chat": message,
            "creatorID": "Guest",
        }
    )
    return True

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    history = getChatHistory()
    # form = UploadFileForm()
    # if form.validate_on_submit():
    #     # Save uploaded file
    #     file = form.file.data
    #     file_path = os.path.join(
    #         os.path.abspath(os.path.dirname(__file__)),
    #         app.config['UPLOAD_FOLDER'],
    #         secure_filename(file.filename)
    #     )
    #     file.save(file_path)

    #     # Generate questions from uploaded file
    #     try:
    #         questions = generate_questions_from_file(file_path, num_questions=5)
    #         if not questions:
    #             return render_template('index.html', form=form, error="No questions could be generated from the file.")
    #         return render_template('index.html', form=form, questions=questions)
    #     except Exception as e:
    #         return render_template('index.html', form=form, error=f"An error occurred: {str(e)}")
    return render_template('index.html')

@app.route('/chat-history', methods=['GET'])
def pull_history():
    history = getChatHistory()

if __name__ == '__main__':
    app.run(debug=True)
