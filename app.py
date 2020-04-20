from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd


#Define o caminho relativo da pasta destino
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'uploads')
#Definite qual o unico tipo que pode ser carregado
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'developer'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def csv_to_dict(arquivo_csv):
    df = pd.read_csv(arquivo_csv,sep =',')
    dic_elementos = pd.DataFrame.to_dict(df, orient='index')
    return dic_elementos;


@app.route('/file', methods=['GET'])
def index():
    return render_template('index.html')

#Uso para testar se a extensão informada é mesmo um csv
def allowed_file(filename): # arq.csv
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#Realiza o upload do arquivo
@app.route('/file/uploaded', methods=['POST'])
def upload_file():
    if 'csv' not in request.files:
        return 'O csv não pode ser enviado!'
    file = request.files['csv']
    if file.filename == '':
        return 'Arquivo não selecionado'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        dict_resul = csv_to_dict(file)
    return redirect(url_for('index'))


@app.route('/')
def hello_world():
    return 'Input CSV: /file'


if __name__ == '__main__':
    app.run()
