#TCPclient.py
# coding: utf-8

import socket
import json

serverName = '127.0.0.1'
serverPort = 50000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#enviado dados depois de estabelecer conexão
messageJson = {}
messageJson['iniciar'] = True
messageJson['reiniciar'] = False
messageJson['dificuldade'] = 'M'
messageJson['linha'] = -1
messageJson['fim'] = False

message = json.dumps(messageJson)

clientSocket.send(message.encode('utf-8'))

modifiedMessage = clientSocket.recv(1024)

print(modifiedMessage.decode('utf-8'))


messageJson['iniciar'] = False

clientSocket.close()

while(True):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    messageJson['linha'] = input("Linha:")
    messageJson['coluna'] = input("coluna:")
    
    message = json.dumps(messageJson)
    clientSocket.send(message.encode('utf-8'))
    modifiedMessage = clientSocket.recv(1024)
    resposta = modifiedMessage.decode('utf-8')
    jsonResposta = json.loads(resposta)
   
    clientSocket.close()
    if(jsonResposta['resposta']['valor']== -1):
        print("Você perdeu")
        break
    else:
        print("\nValor da casa: ",jsonResposta['resposta']['valor'] )