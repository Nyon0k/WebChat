class Chat():
    def __init__(self, chatname, nickname):
        self.chatname = chatname
        self.owner = nickname
        self.connecteds = {}
        self.msg_history = {}
        self.msg_counter = 0

    def dadosChat(self):
        dados = {
            'chatname': self.chatname,
            'criador': self.owner,
        }
        return dados

    def conecta(self, nickname, ip, porta):
        self.connecteds[nickname] = [ip, porta]
        print(f'<chat: {self.chatname} - usuario conectado: {nickname, ip, porta}>')

    def desconecta(self, nickname):
        self.connecteds.pop(nickname)

    def membros(self):
        return self.connecteds

    def historico(self):
        return self.msg_history

    def novaMsg(self, msg, nickname):
        self.msg_counter += 1
        self.msg_history[self.msg_counter] = [nickname, msg]

def encerraChat():
    return