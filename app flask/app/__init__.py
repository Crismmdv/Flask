from flask import Flask
app=Flask(__name__)

form app import views

app.config['SECRET_KEY']='botonsecreto'
app.config['UPLOAD_FOLDER']='static/files'


class UploadFileForm(FlaskForm):
    file= FileField("File", validators=[InputRequired()])
    submit= SubmitField("Upload File")