# -*- encoding: utf-8 -*-

''' Classe Chat, que armazena informações sobre um chat (sala).
    Usada como auxílio pelas demais classes da aplicação.
'''

class Chat():
    def __init__(self, chatname, clientOwner, tSenha = False):
        self.chatname = chatname
        self.owner = clientOwner
        self.senha = tSenha        
        
        # Dicionário com a mesma estrutura do self.connections do Servidor, só que armazena clientes conectadas num chat. 
        self.connecteds = {} # Key: nickname. Value: [ip, porta]
        
        self.msg_history = ""
        
        # String para armazenar a ultima mensagem recebida no chat
        self.msg_recebida = ""
        
        # Dicionário que armazena os frames de vídeo transmistidos por cliente do chat (sala)
        self.clientes_frames = {} # Key: clientname. Value: bytes dos frames de video desse cliente
        
    def dadosChat(self):
        dados = {
            'chatname': self.chatname,
            'criador': self.owner,
            'senha': self.senha
        }
        return dados

    def conectar(self, clientname, ip_cliente, porta_cliente):
        print(f'<chat: {self.chatname} - usuario conectado: {clientname, ip_cliente, porta_cliente}>')
        self.connecteds[clientname] = [ip_cliente, porta_cliente]

    def desconectar(self, clientname):
        self.connecteds.pop(clientname)

    def membros(self):
        return self.connecteds

    def historico(self):
        return self.msg_history

    def getLastMessage(self):
        return self.msg_recebida

    def novaMsg(self, msg, clientname):
        self.msg_history += clientname + ": " + msg + '\n'

    def msgRecebida(self, msg, clientname):
        self.msg_recebida = clientname + " diz: " + msg + '\n'
    
    # Se o transmissor for o mesmo, atualiza os frames dele
    def novoTransmissor(self, clientname, frameBytes):
        self.clientes_frames[clientname] = frameBytes
        
    # Retorna uma lista de transmissores de video num chat
    def getTransmissoresVideo(self):
        return self.clientes_frames.keys()
