import rpyc
from rpyc.utils.server import ThreadedServer
from pickle import TRUE
import time
from chat import Chat

SERVIDOR = '172.24.18.83'
PORTA = 9000

# classe que implementa o servico de echo
class WebChat(rpyc.Service):
    def __init__(self, ip, porta):
        self.ip = ip
        self.porta = porta
        self.connections = [] # pessoas conectadas
        self.chats = {} # nomes dos chats que existem: tupla(chatname, dono)
        self.chat_connections = [] # Pessoas conectadas em cada chat: tupla(chatname, [pessoas])
        self.msg_chat_history = [] # tupla(chatname, [msgs])

	# executa quando uma conexao eh criada
    def on_connect(self, conn):
        print(f'<connected: {self.ip}, {self.porta}>')
        pass

	# executa quando uma conexao eh fechada
    def on_disconnect(self, conn):
        print(f'<disconnected: {self.ip}, {self.porta}>')
        pass

    def exposed_verificaNickname(self, nickname):
        for n in self.connections:
            if n == nickname:
                return False
        return True

    def exposed_abreConexao(self, nickname):
        self.connections.append(nickname)
        # adiciona nickname da pessoa em self.connections

    def exposed_fechaConexao(self, nickname):
        self.connections.remove(nickname)
        # remove nickname da pessoa em self.connections

    def exposed_verPessoasConectadas(self):
        return self.connections

    def exposed_criaChat(self, chatname, nickname):
        for chat in self.chats:
            if chat == chatname:
                return 'ERRO: Nome de chat já utilizado'
        chat = Chat(chatname, nickname)
        print(chat.chatname, chat.owner, chat.connecteds, chat.msg_history)
        self.chats[chatname] = Chat(chatname, nickname)
        print(f'<chat criado: {chatname}>')
        # adiciona o chatname em self.chats, sendo o criador setado como dono
        return

    def exposed_verChats(self):
        return self.chats

    def exposed_entraChat(self, chatname):
        chat = self.chats[chatname]
        dados = chat.dadosChat()
        print(dados)
        return dados

    def exposed_mandaMsg():
        return

    # notifica todos as pessoas conectadas no chat com a nova msg
    def exposed_compartilhaMsg(self, notifica, msg):
        return notifica(msg)

    def exposed_compartilhaImg(self):
        return
    
def iniciaServer(servidor, porta):
    srv = ThreadedServer(WebChat(servidor, porta), port = porta)
    print('----- Server inicializado -----')
    srv.start()

iniciaServer(SERVIDOR, PORTA)