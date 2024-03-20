from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from googletrans import Translator
import pickle

import sys

sys.path.append("../../")

from dotenv import load_dotenv
import os

colunas = ['tamanho', 'ano', 'garagem']

modelo = pickle.load(open('../../models/modelo.sav', 'rb'))

app = Flask(__name__)

# Realizando a autenticação 
app.config['BASIC_AUTH_USERNAME'] = os.getenv('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

# Definindo rotas
@app.route('/')
def home():
    return "Minha Primeira APII"

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    translator = Translator()
    frase_en = translator.translate(frase, dest='en')
    tb_en = frase_en.text
    tb = TextBlob(tb_en)
    polaridade = tb.sentiment.polarity
    return f"Polaridade: {polaridade}"


@app.route('/cotacao/', methods=['POST'], endpoint='cotacao')
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True, host='0.0.0.0')

# Para funcionar basta executar: python main.py