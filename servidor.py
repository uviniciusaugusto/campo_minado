import random

import socket
import json

serverPort = 50000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.bind(('',serverPort))
serverSocket.listen(0)

jogadores = [];
jsonJogadores = {};

campos = [];

posicoes = [];
coord = [];

resposta = {};
pontuacoes = []

rodadas = 0
print("Servidor pronto para recever")

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Conexão vinda de {}".format(addr))
    message = connectionSocket.recv(2048)
    print ("{} ==> {}".format(addr, message.decode("utf-8")))
    idJogador = format(addr)
    dados = json.loads(message.decode("utf-8"))

    if (idJogador not in jogadores):
        jogadores.append(idJogador)
        pontuacoes[idJogador] = 0
        json[idJogador] = {}
        json[idJogador]['pontos'] = 0
        json[idJogador]['conexao'] = connectionSocket

    if(dados['reiniciar'] == True):
        campos = []
    
    if(dados['iniciar'] == True):
        
        tamGrid = dados['dificuldade']

        grid = 0
        bombas = 0 

        if tamGrid == 'F':
            grid = 5
            bombas = 3
        elif tamGrid== 'M':
            grid = 6
            bombas = 8
        else:
            grid = 8
            bombas = 20
        
        score = 0;
        campos = gerarCampoMinado(grid + len(jogadores), bombas + len(jogadores));
    
    elif(dados['linha'] != -1):
        rodadas += 1
        linha = (dados['linha']);
        coluna = (dados['coluna']);

        if(campos[linha][coluna] != 'B'):
            json[idJogador]['pontos'] += 1
            pontuacoes[idJogador] = json[idJogador]['pontos']
        
        coord = [];
        coord.append(linha);
        coord.append(coluna);
        posicoes.append(coord);
        i = 0
        ranking = sorted(pontuacoes, reverse=True)
        while(i < len(pontuacoes)):
            if(pontuacoes[idJogador]==ranking[i]):
                colocacao = i;
                break;
        
        resposta = {
            "posicoes" : posicoes,
            "valor": campos[linha][coluna],
            "qtdJogadores" : len(jogadores),
            'posicaoNaPartida' : colocacao,
            'rodadas' : rodadas
        }
    
    elif(dados['linha'] == -1):
        resposta = {
            "posicoes" : posicoes,
        }
    
    jsonJogadores[idJogador]['resposta'] = resposta
        
    for j in jogadores:
        jsonJogadores[j]['conexao'].send(jsonJogadores.encode("utf-8"))

    connectionSocket.close()
    


def gerarCampoMinado(g, b):
    campos = [[0 for row in range(g)] for column in range(g)]
    for num in range(b):
        x = random.randint(0,g-1)
        y = random.randint(0,g-1)
        arr[y][x] = 'B'
        if (x >=0 and x <= g-2) and (y >= 0 and y <= g-1):
            if campos[y][x+1] != 'B':
                campos[y][x+1] += 1 
        if (x >=1 and x <= g-1) and (y >= 0 and y <= g-1):
            if campos[y][x-1] != 'B':
                campos[y][x-1] += 1 
        if (x >= 1 and x <= g-1) and (y >= 1 and y <= g-1):
            if campos[y-1][x-1] != 'B':
                campos[y-1][x-1] += 1 
 
        if (x >= 0 and x <= g-2) and (y >= 1 and y <= g-1):
            if campos[y-1][x+1] != 'B':
                campos[y-1][x+1] += 1
        if (x >= 0 and x <= g-1) and (y >= 1 and y <= g-1):
            if campos[y-1][x] != 'B':
                campos[y-1][x] += 1 
 
        if (x >=0 and x <= g-2) and (y >= 0 and y <= g-2):
            if campos[y+1][x+1] != 'B':
                campos[y+1][x+1] += 1 
        if (x >= 1 and x <= g-1) and (y >= 0 and y <= g-2):
            if campos[y+1][x-1] != 'B':
                campos[y+1][x-1] += 1 
        if (x >= 0 and x <= g-1) and (y >= 0 and y <= g-2):
            if campos[y+1][x] != 'B':
                campos[y+1][x] += 1
    return campos