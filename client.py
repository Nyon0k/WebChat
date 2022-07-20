import multiprocessing
from queue import Empty
from sys import flags
import rpyc
from rpyc.utils.server import ThreadedServer
import time
from chat import Chat
import cv2, imutils, pickle

SERVIDOR = '127.0.0.1'
PORTA = 9000 

##### Server Client #####

# classe que implementa o servico de echo
class Client(rpyc.Service):
    def __init__(self, ip, porta):
        self.ip = ip
        self.porta = porta
        self.connections = [] # pessoas conectadas
        self.chats = {} # nomes dos chats que existem: tupla(chatname, dono)
        self.chat_connections = [] # Pessoas conectadas em cada chat: tupla(chatname, [pessoas])
        self.msg_chat_history = [] # tupla(chatname, [msgs])

	# executa quando uma conexao eh criada
    def on_connect(self, conn):
        # print(f'<connected: {self.ip}, {self.porta}>')
        pass

	# executa quando uma conexao eh fechada
    def on_disconnect(self, conn):
        # print(f'<disconnected: {self.ip}, {self.porta}>')
        pass

    # Quando um chat for atualizado no servidor central,
    # esse método é chamando para mostrar a nova msg para o cliente
    def exposed_recebeMsg(self, msg, nickname):
        print(f'{nickname}: {msg}')

    # Análogo ao metodo de cima
    def exposed_recebeImg(self, frame, nickname):
        # print(frame)
        cv2.imshow(f'{nickname}', frame) # show video frame at client side
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            return

    def iniciaConexao(PORTA):
        conn = rpyc.connect(SERVIDOR, PORTA)
        return conn

    def verificaNickname(conn, nickname):
        res = conn.root.exposed_verificaNickname(nickname)
        print(res)
        return res

    # envia imagem de video para o servidor
    def enviaVideo(flag, chatname, nickname):
        while True:
            print(f'<cam connect: {chatname}, {nickname}>')
            if flag:
                vid = cv2.VideoCapture(-1)
                while (vid.isOpened()):
                    img, frame = vid.read()
                    frame = imutils.resize(frame, width=320)
                # while True:
                    # frame = 'oi'
                    try:
                        connTemp = rpyc.connect(SERVIDOR, 5000)
                        connTemp.root.compartilhaImg(frame, chatname, nickname)
                        connTemp.close()
                    except Exception as e:
                        print(e)
                        raise Exception(e)

                    cv2.imshow('<transmitindo video>', frame) # will show video frame on server side.
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        return

def iniciaServerClient(servidor, porta):
    srv = ThreadedServer(Client(servidor, porta), port = porta)
    print('----- <ServerClient> -----')
    srv.start()

def inicializador(porta):
    SERVER = multiprocessing.Process(target = iniciaServerClient, args = (SERVIDOR, porta))
    SERVER.start()
    inicio(porta)

def menu():
    print('-----| Menu |-----')
    print('1 - Ver pessoas conectadas')
    print('2 - Ver chats')
    print('3 - Criar chat')
    print('4 - Entrar em um chat')
    print('0 - Sair')
    print('----------------')
    print('Escolha uma opção do menu:')

def chatMenu():
    print('-----| Menu do chat |-----')
    print('/m - <Mostrar membros do chat>')
    print('/h - <Mostrar histórico de mensagens>')
    print('/d - <Mostrar dados do chat>')
    print('/won - <Abrir camera>')
    print('/woff - <Fechar camera>')
    print('/exit - <Para sair do chat>')
    print('--------------------------')
    print('Digite uma opção do menu:')

def inicio(porta):
    conn = Client.iniciaConexao(5000)
    print('<Bem vindo ao WebChat>')
    print('Digite seu nickname:')
    while True:
        nickname = input()
        if Client.verificaNickname(conn, nickname) == True:
            conn.root.abreConexao(nickname, SERVIDOR, porta)
            break
        print('Nome já utilizado, escolha outro:')
    menu()
    while True:
        escolha = int(input())
        if escolha == 1:
            res = conn.root.verPessoasConectadas()
            print(res)
        if escolha == 2:
            res = conn.root.verChats()
            print(res)
        if escolha == 3:
            print('Digite o nome do chat que deseja criar:')
            chatname = input()
            # print('Deseja senha? (s) ou (n):')
            # tem_senha = input()
            res = conn.root.criaChat(chatname, nickname)
            print(res)
            menu()
        if escolha == 4:
            print('Digite o nome do chat que deseja entrar:')
            chatname = input()
            res = conn.root.entraChat(chatname, nickname)
            chatMenu()
            print(f'Conectado no chat: ({chatname})')
            while True:
                msg = input()
                if msg == '/m':
                    res = conn.root.membrosChat(chatname)
                    print('<membros>')
                    print(res)
                    print('---------')
                if msg == '/h':
                    res = conn.root.historicoDoChat(chatname)
                    print('<chat atualizado>')
                    for n in res:
                        print(f'{res[n][0]}: {res[n][1]}')
                if msg == '/d':
                    res = conn.root.dadosChat(chatname)
                    print('<dados chat>')
                    print(res)
                    print('------------')
                if msg == '/won':
                    flag = True
                    # img_process = Client.enviaVideo(flag, chatname, nickname)
                    img_process = multiprocessing.Process(target = Client.enviaVideo, args = (flag, chatname, nickname))
                    img_process.start()
                    print('Abriu Vídeo')
                if msg == '/woff':
                    img_process.terminate()
                    print(f'<cam disconnect: {chatname}, {nickname}>')
                if msg == '/exit':
                    conn.root.saiChat(chatname, nickname)
                    menu()
                    break
                if msg != '/m' or msg != '/h' or msg != '/exit':
                    ret = conn.root.compartilhaMsg(msg, chatname, nickname)
                    ret
        if escolha == 0:
            conn.root.exposed_fechaConexao(nickname)
            break

def main():
    PORTA = input('Digite sua porta: ')
    inicializador(PORTA)

main()

'''ChatVideo'''

#### Client ####

# import socket, pickle, struct
# import cv2

# # create socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_ip = '172.24.16.1'  # paste your server ip address here
# port = 9999
# client_socket.connect((host_ip, port))  # a tuple
# data = b""
# payload_size = struct.calcsize("Q") # Q: unsigned long long integer(8 bytes)

# #Business logic to receive data frames, and unpak it and de-serialize it and show video frame on client side
# while True:
#     while len(data) < payload_size:
#         packet = client_socket.recv(4 * 1024)  # 4K, range(1024 byte to 64KB)
#         if not packet: break
#         data += packet # append the data packet got from server into data variable
#     packed_msg_size = data[:payload_size] #will find the packed message size i.e. 8 byte, we packed on server side.
#     data = data[payload_size:] # Actual frame data
#     msg_size = struct.unpack("Q", packed_msg_size)[0] # meassage size
#     # print(msg_size)

#     while len(data) < msg_size:
#         data += client_socket.recv(4 * 1024) # will receive all frame data from client socket
#     frame_data = data[:msg_size] #recover actual frame data
#     data = data[msg_size:]
#     frame = pickle.loads(frame_data) # de-serialize bytes into actual frame type
#     cv2.imshow("RECEIVING VIDEO", frame) # show video frame at client side
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'): # press q to exit video
#         break
# client_socket.close()

#### Server ####

# # This code is for the server
# # Lets import the libraries
# import socket, cv2, pickle, struct, imutils

# # Socket Create
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
# host_ip = '172.24.16.1'
# print('HOST IP:', host_ip)
# port = 9999
# socket_address = (host_ip, port)

# # Socket Bind
# server_socket.bind(socket_address)

# # Socket Listen
# server_socket.listen(5)
# print("LISTENING AT:", socket_address)


# # Socket Accept
# while True:
#     client_socket, addr = server_socket.accept()
#     print('GOT CONNECTION FROM:', addr)
#     if client_socket:
#         vid = cv2.VideoCapture(0)

#         while (vid.isOpened()):
#             img, frame = vid.read()
#             frame = imutils.resize(frame, width=320)
#             a = pickle.dumps(frame) #serialize frame to bytes
#             message = struct.pack("Q", len(a)) + a # pack the serialized data
#             print(message)
#             try:
#                 client_socket.sendall(message) #send message or data frames to client
#             except Exception as e:
#                 print(e)
#                 raise Exception(e)


#             cv2.imshow('TRANSMITTING VIDEO', frame) # will show video frame on server side.
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 client_socket.close()