import random
import socket
import json

#Função responsavel por montar a matriz do campo minado
def gerarCampoMinado(g, b):
    campos = [[0 for row in range(g)] for column in range(g)]
    for num in range(b):
        x = random.randint(0,g-1)
        y = random.randint(0,g-1)
        campos[y][x] = -1
        if (x >=0 and x <= g-2) and (y >= 0 and y <= g-1):
            if campos[y][x+1] != -1:
                campos[y][x+1] += 1 
        if (x >=1 and x <= g-1) and (y >= 0 and y <= g-1):
            if campos[y][x-1] != -1:
                campos[y][x-1] += 1 
        if (x >= 1 and x <= g-1) and (y >= 1 and y <= g-1):
            if campos[y-1][x-1] != -1:
                campos[y-1][x-1] += 1 
 
        if (x >= 0 and x <= g-2) and (y >= 1 and y <= g-1):
            if campos[y-1][x+1] != -1:
                campos[y-1][x+1] += 1
        if (x >= 0 and x <= g-1) and (y >= 1 and y <= g-1):
            if campos[y-1][x] != -1:
                campos[y-1][x] += 1 
 
        if (x >=0 and x <= g-2) and (y >= 0 and y <= g-2):
            if campos[y+1][x+1] != -1:
                campos[y+1][x+1] += 1 
        if (x >= 1 and x <= g-1) and (y >= 0 and y <= g-2):
            if campos[y+1][x-1] != -1:
                campos[y+1][x-1] += 1 
        if (x >= 0 and x <= g-1) and (y >= 0 and y <= g-2):
            if campos[y+1][x] != -1:
                campos[y+1][x] += 1
    return campos

serverPort = 50000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.bind(("127.0.0.1",serverPort))
serverSocket.listen(0)

jogadores = [];
jsonJogadores = {};
campos = [];
posicoes = [];
coord = [];
resposta = {};
pontuacoes = []
rodada = 0;
rodadas = 0
print("Servidor pronto para recever")

while True:
    #Recebe a conexão
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(2048)
    idJogador = format(addr)
    #Decodifica a mensagem
    mensagem = message.decode("utf-8")
  
    dados = json.loads(mensagem)

    if(dados['fim'] == True):
        break;
    
    #Acrescenta os dados dos jogadores nas estruturas
    if (idJogador not in jogadores):
        jogadores.append(idJogador)
        pontuacoes.append(0)

        jsonJogadores[idJogador] = {}
    
    if(dados['reiniciar'] == True):
        campos = []
    
    if(dados['iniciar'] == True or len(campos)<1):
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
        linha = int(dados['linha']);
        coluna = int(dados['coluna']);
        
        if(campos[linha][coluna] != -1):
            pontuacoes[0] += 1
        
        coord = [];
        coord.append(linha);
        coord.append(coluna);
        posicoes.append(coord);
        colocacao = 1
        
        resposta = {
            "pontuacao" : pontuacoes[0],
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
    jsonJogadores['resposta'] = resposta
    

    #Definição de qual jogador deverá jogar
    rodada += 1
    if(rodada >= len(jogadores)):
        rodada = 0
    for j in jogadores:
        jsonJogadores[j]['suaVez'] = False
    jsonJogadores[jogadores[rodada]]['suaVez'] = True
    
    #Conversão e envio dos dados
    message = json.dumps(jsonJogadores)
    connectionSocket.send(message.encode("utf-8"))

    #Fechamento da conexão
    connectionSocket.close()

