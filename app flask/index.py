from contextlib import redirect_stderr
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
#from requests import request as rqt
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import pandas as pd
from funciones import creardf_sc, creardf_piper
from piper import plotpiper

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
        ruta3= os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
        #ruta2= os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename('archivo.csv'))
        file.save(ruta3)
        tit= creardf_sc(pd.read_csv(ruta3,','))
        
        #titulos= tit.to_csv(ruta2)
        session["ruta"]=ruta3
        return redirect(url_for('Tablas'))

    return render_template('Datos.html',form=form)
@app.route('/Tablas', methods=['GET','POST'])
def Tablas():
    elementos=()
    if "ruta" in session:
        ruta=session["ruta"] 
        try: 
            tit = pd.read_csv(ruta)
            #session["CSV"]=tit
            dtipo= tit.dtypes
            dindex=list(dtipo.index)
            dvalues=list(dtipo.values.astype(str))
            dtipo= dict( pd.Series(dvalues, index= dindex))
            session['dtipo']=dtipo
        except: titulos=''
    else: titulos='error'
    titulos= tit.columns.values
    if request.method =='POST':
        
        lista_de_tabla=list()    
        
        tg= request.form['tipog']
        session["tipograf"]=tg
        if tg == "Schoeller":
            elementos = ('Cu', 'Cr','F', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS')
        elif tg== "Piper":
            elementos= ('Cl','SO4','HCO3','CO3','Na','Ca','Mg','K')
        elif tg== "Gibbs":
            elementos= ('Cl','HCO3','Na','Ca','TDS')
        session["elementos"]=elementos
        
        
        next = tg!=''
        #print (dtipo)
        if next:
            return redirect(url_for('Validacion'))
        return render_template('carga.html',tabla=titulos,elem=elementos,cabecera="Error")
    return render_template('cargapiper.html',tabla=titulos,elem=elementos)   


@app.route('/Visor')
def Visor():
    graficos=("Schoeller","Piper", "Stiff")
    return render_template('visor.html', tipografico=graficos)

@app.route('/Prueba')
def Prueba():
    

    if request.method =='POST':
        elementos=session["elementos"]

                            
        return render_template('clear.html')
    return redirect(url_for('Visor'))

def new_func():
    lista_de_tablas=list()

@app.route('/Validacion', methods=['GET','POST'])
def Validacion():
    elementos=session["elementos"]
    
    titulos= list(session["dtipo"].keys())
    dtipo= session["dtipo"]
    tg=session["tipograf"]
    session["tipograf"]=tg
            
    if request.method=='POST':
        llaves=list()
        for elm in elementos:
            llaves.append((elm,request.form[elm]))
            #print (request.form[elm])
        next=True
        session["llaves"]=dict(llaves)
        return redirect(url_for('Grafico'))
        
    return render_template('carga.html',tabla=titulos,elem=elementos,cabecera='Parámetros '+tg, dtip=dtipo)

@app.route('/Grafico', methods=['GET','POST'])
def Grafico():
    dicc=session["llaves"]
    ruta=session["ruta"] 
    tit = pd.read_csv(ruta)
    Y_df=tit
    format_df= creardf_piper(Y_df,'','',25, dicc)
    filtro=''
    filtro2=''
    img=plotpiper(format_df, unit='mg/L', figname='Piper '+filtro+'_'+filtro2+'_Subcuenca', figformat='jpg',nc=1)
    
    return render_template('clear.html',df=img)


if __name__=='__main__':
    app.run(debug=True)



