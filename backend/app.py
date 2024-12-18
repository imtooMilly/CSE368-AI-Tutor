from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from question_generation import generate_questions_from_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Generate Quiz")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        # Save uploaded file
        file = form.file.data
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'],
            secure_filename(file.filename)
        )
        file.save(file_path)

        # Generate questions and MCQs from uploaded file
        try:
            quiz_data = generate_questions_from_file(file_path, num_questions=5)

            if not quiz_data['questions'] and not quiz_data['mcqs']:
                return render_template('index.html', form=form, error="No questions could be generated from the file.")

            return render_template(
                'index.html',
                form=form,
                questions=quiz_data['questions'],  # Open-ended questions
                mcqs=quiz_data['mcqs']  # Multiple-choice questions
            )
        except Exception as e:
            return render_template('index.html', form=form, error=f"An error occurred: {str(e)}")

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)