from time import timezone
import jwt
from jwt import InvalidSignatureError
import datetime
from datetime import timezone

#Chaves
chave_privada = open("chaveprivada.pem", 'r').read()
chave_publica = open("chavepublica.pem", 'r').read()


vencimento_token = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=1)

#Payload
payload_data = {"nome": "teste","sub": "teste", "exp": vencimento_token}

gera_token = jwt.encode(payload=payload_data, key=chave_privada, algorithm="RS256")

print("token: ", gera_token)

try:
    decoded = jwt.decode(gera_token, chave_publica , algorithms="RS256")
    print(decoded)
except InvalidSignatureError as e:
    print(e)
