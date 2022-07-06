class Chat():
    def __init__(self, chatname, nickname):
        self.chatname = chatname
        self.owner = nickname
        self.connecteds = []
        self.msg_history = []

    def dadosChat(self):
        dados = {
            'chatname': self.chatname,
            'criador': self.owner,
            'conectados': self.connecteds,
            'histórico': self.msg_history
        }
        return dados

    def entraChat(self):
        print('foi')

def encerraChat():
    return