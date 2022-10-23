from fastapi import FastAPI
from dto.conexao import consultaCli
from dto.conexao import atualizaCli
from pydantic import BaseModel
from typing import Union
import requests
import jwt

app = FastAPI()

# Classe de dados de entrada
class DadosCliente(BaseModel):
    iddadosCli: Union[int, None] = None
    rNomeCli: Union[str, None] = None
    rEmail: Union[str, None] = None
    nIdade: Union[int, None] = None
    rLogradouro: Union[str, None] = None
    nCep: Union[str, None] = None
    rBairro: Union[str, None] = None
 
#Criando APIs
@app.get("/verDadosCliente")
def consultaDadosCliente(cliente):
    """Consultando dados cliente"""
    consultarCliente = consultaCli(cliente)
    return consultarCliente

@app.post("/AtualizarDados")
def atualizaDados(dadosCliente: DadosCliente):
    """Atualizando dados do cliente"""
    #Consulta dados do cliente e caso o usuario nao passe algum atributo será utilizado o mesmo valor ja existente na base.
    consultarCliente = consultaCli(dadosCliente.iddadosCli)
    if (consultarCliente['Nome'] != None) and (dadosCliente.rNomeCli == None or dadosCliente.rNomeCli == "string"):
         dadosCliente.rNomeCli = consultarCliente['Nome']
    if (consultarCliente['Email'] != None) and (dadosCliente.rEmail == None or dadosCliente.rEmail == "string"):
        dadosCliente.rEmail = consultarCliente['Email']
    if (consultarCliente['Idade'] != None) and (dadosCliente.nIdade == None or dadosCliente.nIdade == "string"):
        dadosCliente.nIdade = consultarCliente['Idade']
    if (consultarCliente['End'] != None) and (dadosCliente.rLogradouro == None or dadosCliente.rLogradouro == "string"):
        dadosCliente.rLogradouro = consultarCliente['End']
    if (consultarCliente['Cep'] != None) and (dadosCliente.nCep == None or dadosCliente.nCep == "string"):
        dadosCliente.nCep = consultarCliente['Cep']
    if (consultarCliente['Bairro'] != None) and (dadosCliente.rBairro == None or dadosCliente.rBairro == "string"):
        dadosCliente.rBairro = consultarCliente['Bairro']

    #Atualiza dados do cliente
    atualizarCliente = atualizaCli(dadosCliente.iddadosCli, dadosCliente.rNomeCli, dadosCliente.rEmail, dadosCliente.nIdade, dadosCliente.rLogradouro, dadosCliente.nCep, dadosCliente.rBairro)
    if atualizarCliente != "":
        saidac = dadosCliente.dict()
        return saidac
    else:
        saidaE = "Erro ocorrido"
        return saidaE

@app.post("/AcessaApiParceiro")
def acessaApiParceiro(dadosCliente: DadosCliente):
    if len(dadosCliente.nCep) == 8:
        apiResponse = requests.get('https://viacep.com.br/ws/{}/json/'.format(dadosCliente.nCep)).json()
        if  apiResponse != None or apiResponse != "":
            dadosCliente.rLogradouro = apiResponse['logradouro']
            dadosCliente.nCep = apiResponse['cep']
            dadosCliente.rBairro = apiResponse['bairro']
            atualizaDados(dadosCliente)
            return apiResponse
    else:
        mensagem = {"erro": 401,"msg": "O Cep Informado não é válido, deve ser digitado sem pontuação"}
        return  mensagem

#Realizando debbug dos metodos
#if __name__ == '__main__':
#   consultaDadosCliente(1)
#    objeto_carregado = DadosCliente(iddadosCli = 2, rNomeCli = None, rEmail = None, nIdade = None, rLogradouro = None, nCep = '72854005', rBairro = None)
#    objeto_carregado = DadosCliente(iddadosCli = 2, nCep = '72854005')
#    acessaApiParceiro(objeto_carregado)  