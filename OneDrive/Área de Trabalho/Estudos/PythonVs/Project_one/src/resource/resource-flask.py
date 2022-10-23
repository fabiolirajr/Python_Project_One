from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from dto.conexao import consultaCli
from dto.conexao import atualizaCli
from pydantic import BaseModel
from typing import Union
import requests
import datetime

app = Flask(__name__)

# Lendo a PRIVATE_KEY para assinar token:
chave_privada = open("chaveprivada.pem", 'r').read()
# Lendo a PUBLIC_KEY para verificar token:
chave_publica = open("chavepublica.pem", 'r').read()

app.config["JWT_PRIVATE_KEY"] = chave_privada
app.config["JWT_PUBLIC_KEY"] = chave_publica
app.config['JWT_ALGORITHM'] = 'RS256'

# Esse será o intervalo de tempo de expiração do token:

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

jwt = JWTManager(app)

#Autenticação
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Username ou senha incorretos"}), 401
        # Você precisa proteger contra ataque de força bruta.
        # Pode contar quantas vezes um usuário tentou logar com erro.
        # e/ou pode enviar um CAPTCHA a ele.

    access_token = create_access_token(identity=username)

    # O default é retornar o token no corpo do request. 
    # O cliente tem que enviar um header "Authorization: Bearer <token>"

    return jsonify(access_token=access_token)


#Criando APIs
# O decorator @jwt_required protege a rota contra acesso anônimo, ele será o responsável por obrigar que seja enviado o header Authorization, com o access-token obtido na api /login.

@app.route("/verDadosCliente", methods=["GET"])
@jwt_required()
def consultaDadosCliente():
    """Consultando dados cliente"""
    cliente = request.headers.get('cliente')
    consultarCliente = consultaCli(cliente)
    return consultarCliente

@app.route("/AtualizarDados", methods=["POST"])
@jwt_required()
def atualizaDados():
    """Atualizando dados do cliente"""

    codigoServico = None
    #Recebe body request(Em formato JSON)

    dadosCliente = request.get_json()

    #Verificando se foi enviado os campos no request body
    if dadosCliente:
        if 'Id' in dadosCliente:
            Id = dadosCliente['Id']
        else:
            Id = None

        if 'Nome' in dadosCliente:
            Nome = dadosCliente['Nome']
        else:
            Nome = None

        if 'Email' in dadosCliente:
            Email = dadosCliente['Email']
        else:
            Email = None

        if 'Idade' in dadosCliente:
            Idade = dadosCliente['Idade']
        else:
            Idade =  None
        
        if 'End' in dadosCliente:
            End = dadosCliente['End']
        else:
            End = None
        
        if 'Cep' in dadosCliente:  
            Cep = dadosCliente['Cep']
        else:
            Cep = None
        
        if 'Bairro' in dadosCliente:
            Bairro = dadosCliente['Bairro']
        else:
            Bairro = None


    #Consulta dados do cliente e caso o usuario nao passe algum atributo será utilizado o mesmo valor ja existente na base.
    consultarCliente = consultaCli(Id)
    if (consultarCliente['Nome'] != None) and (Nome == None):
         Nome = consultarCliente['Nome']
    if (consultarCliente['Email'] != None) and (Email == None):
        Email = consultarCliente['Email']
    if (consultarCliente['Idade'] != None) and (Idade== None):
        Idade = consultarCliente['Idade']
    if (consultarCliente['End'] != None) and (End == None):
        End = consultarCliente['End']
    if (consultarCliente['Cep'] != None) and (Cep == None):
        Cep = consultarCliente['Cep']
    if (consultarCliente['Bairro'] != None) and (Bairro == None):
        Bairro = consultarCliente['Bairro']

    #Atualiza dados do cliente
    atualizarCliente = atualizaCli(Id, Nome, Email, Idade, End, Cep, Bairro)
    if atualizarCliente != "":
        saidac = dadosCliente
        return jsonify(saidac)
    else:
        saidaE = "Erro ocorrido"
        return saidaE

@app.route("/buscaEnderecoPorCep", methods=["POST"])
@jwt_required()
def acessaApiParceiro():
    dadosCliente = request.get_json()
    #Instancia as variaveis

    if dadosCliente:
        if 'Cep' in dadosCliente:
            Cep = dadosCliente['Cep']
    else:
        return "Cep não informado"

    if len(Cep) == 8:
        apiResponse = requests.get('https://viacep.com.br/ws/{}/json/'.format(Cep))
        if apiResponse.status_code != 200:
            if apiResponse.status_code == 500:
                mensagem = jsonify({"erro": 500,"msg": "Internal server error"}), 500
                return mensagem
            if apiResponse.status_code == 400:
                mensagem = jsonify({"erro": 400,"msg": "CEP INVALIDO"}), 400
                return  mensagem
        else:
            return apiResponse.json()         
    else:
        mensagem = jsonify({"erro": 400,"msg": "O Cep Informado não é válido, deve ser digitado sem pontuação"}), 400
        return  mensagem

#Realizando debbug dos metodos
if __name__ == '__main__':
#   consultaDadosCliente(1)
#    objeto_carregado = DadosCliente(iddadosCli = 2, rNomeCli = None, rEmail = None, nIdade = None, rLogradouro = None, nCep = '72854005', rBairro = None)
#    objeto_carregado = DadosCliente(iddadosCli = 2, nCep = '72854005')
#    acessaApiParceiro(objeto_carregado)  
     app.run()
#   objeto_carregado = {"nIdade": 88, "iddadosCli": 2}
#    atualizaDados()