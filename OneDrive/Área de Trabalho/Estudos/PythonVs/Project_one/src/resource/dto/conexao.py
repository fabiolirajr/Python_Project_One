import mysql.connector
from mysql.connector import Error

def consultaCli(cliente):
    try:
        cnx = mysql.connector.connect(user='', password='', host='', database='')
        cursor = cnx.cursor()
        result = cursor.callproc('sp_consulta_cliente', [cliente,0,"","",0,"","",""])
        resultadoPesquisa = {"Id_cliente": result[1], "Nome": result[2], "Email": result[3], "Idade": result[4], "End": result[5], "Cep": result[6], "Bairro": result[7]}
        return resultadoPesquisa
    except mysql.connector.Error as error:
         ErroSQL = print("Failed to execute stored procedure: {}".format(error))
         return ErroSQL
    finally:
         if (cnx.is_connected()):
            cursor.close()
            cnx.close()  
#Método consultaCli - Acessando direto a base de dados MySQL via Select
#query = ("SELECT * FROM primeiroprojeto.tdadoscli where iddadosCli = {}".format(cliente))
#cursor.execute(query)
#rows = cursor.fetchall()
#return rows

def atualizaCli(iddadosCli, rNomeCli, rEmail, nIdade, rLogradouro, nCep, rBairro):
    try:
        cnx = mysql.connector.connect(user='', password='', host='', database='')
        cursor = cnx.cursor()
        result = cursor.callproc('sp_atualiza_cliente', [iddadosCli, rNomeCli,rEmail,nIdade,rLogradouro,nCep,rBairro])
        cnx.commit()
    except mysql.connector.Error as error:
        ErroSQL = print("Failed to execute stored procedure: {}".format(error))
        return ErroSQL
    finally:
         if (cnx.is_connected()):
            cursor.close()
            cnx.close()

#Método consultaCli - Acessando direto a base de dados MySQL via Select
#query = ("UPDATE primeiroprojeto.tdadoscli SET rNomeCli = '{}', rEmail = '{}', nIdade = {} where iddadosCli = {}".format(rNomeCli, rEmail, nIdade, iddadosCli))
#cursor.execute(query)   