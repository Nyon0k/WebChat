class Chat():
    def __init__(self, chatname, nickname):
        self.chatname = chatname
        self.owner = nickname
        self.connecteds = {}
        self.msg_history = {}
        self.msg_counter = 0
        self.last_msg = ''

    def dadosChat(self):
        dados = {
            'chatname': self.chatname,
            'criador': self.owner,
            'conectados': self.connecteds,
            'histórico': self.msg_history
        }
        return dados

    def conecta(self, nickname, ip, porta):
        self.connecteds[nickname] = [ip, porta]
        print(f'<usuario conectado: {nickname, ip, porta}>')

    def disconecta(self, nickname):
        self.connecteds.remove(nickname)

    def membros(self):
        return self.connecteds

    def historico(self):
        return self.msg_history

    def novaMsg(self, msg, nickname):
        self.msg_counter += 1
        self.msg_history[self.msg_counter] = [nickname, msg]
        self.last_msg = msg

    def ultimaMsg(self):
        return self.last_msg

def encerraChat():
    return