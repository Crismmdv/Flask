from flask import Flask, render_template

app= Flask(__name__)
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
@app.route('/lenguajes')
def mostrarlenguajes():
    return render_template('lenguajes.html')
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__=='__main__':
    app.run(debug=True)

