from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired



app= Flask(__name__)
app.config['SECRET_KEY']='botonsecreto'
app.config['UPLOAD_FOLDER']='static/files'


class UploadFileForm(FlaskForm):
    file= FileField("File", validators=[InputRequired()])
    submit= SubmitField("Upload File")

"""
@app.route('/')
def principal():
    return "Otra vez.."
@app.route('/contacto')
def contacto():
    return ('Esta es la pagina de ctacto')
"""
@app.route('/')
def principal():
    return render_template('index.html')
@app.route('/Datos', methods=['GET','POST'])
def Datos():

    form= UploadFileForm()
    if form.validate_on_submit():
        file= form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return "El archivo fue cargado exitosamente"

    return render_template('Datos.html',form=form)
@app.route('/Visor')
def Visor():
    graficos=("Schoeller","Piper", "Stiff")
    return render_template('visor.html', tipografico=graficos)

if __name__=='__main__':
    app.run(debug=True)

