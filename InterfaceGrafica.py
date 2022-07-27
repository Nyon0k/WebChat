# -*- encoding: utf-8

import tkinter, threading
from Cliente import Cliente
from socket import gethostname, gethostbyname
from time import sleep

class MainWindow:
    ''' Classe que representa a janela principal da GUI '''
    
    # Dicionário que armazena as janelas de chat abertas na GUI
    janelasChat = {} # Key: Chatname. Value: lista [tk root_chat object, chatWindow object]
    
    def __init__(self, master):
        # Atributo que gerencia a janela raiz
        self.janela_root = master
        
        # Variável booleana para armazenar se existe cliente na GUI
        self.existe_cliente_GUI = False # True = existe, False = nexiste
        
        # Variável booleana para armanazenar se a thread para ligar o modo passivo já foi lançada
        # Lançamento deve ocorrer somente 1 única vez
        self.chave_thread_servidorCliente = False # True = sim, False = não
        
        # Variável booleana para armazenar se o cliente está conectado ao Servidor Central
        self.isConectadoServidor = False
            
        # Variável para armazenar o nome do cliente setado no Servidor Central
        self.cli_nickname = None
        
        # Seta uma fonte default para alguns widgets
        self.fonte = ("Arial", 12) 
        
        # Configurações da janela raiz 
        self.setTitle("< Web Chat >")
        self.setSize(600,600)
        master.protocol("WM_DELETE_WINDOW", self._destroy_janela_root)
        
        # Frames 
        self.build_frameLogo()
        self.build_frameConexao()
        self.build_frameNickname()
        self.build_frameChat()
        self.build_frameClientes_Chats()
        
    # Define o título da janela principal #
    def setTitle(self, titulo):
        self.janela_root.title(titulo)
        
    # Define o tamanho da janela principal #
    def setSize(self, width, height):
        size = str(width) + 'x' + str(height)
        self.janela_root.geometry(size)
        # Impede que a janela seja redimensionada
        self.janela_root.resizable(0,0)
    
    # Construção e posicionamento dos widgets 
    
    # Constroi o frame da GUI que exibe o logo
    def build_frameLogo(self):
        fonteLogo = ("Palatino Linotype", 23)
        self.lb_logo = tkinter.Label(self.janela_root, text = " Web Chat ", 
                                     font = fonteLogo, fg = "#062444")
        
        self.lb_logo.pack(pady = 10)
    
    # Constroi o frame da GUI que lida com a conexões do Cliente (Server Client, Servidor Central) #
    def build_frameConexao(self):
        # Constroi o frame
        self.frame_conexao = tkinter.Frame(self.janela_root)
        
        # Constroi os widgets (elementos de janela) do frame_conexao
        self.lb_parametrosServidor = tkinter.Label(self.frame_conexao, 
                                        text = "Parâmetros do Servidor",
                                        font = self.fonte, fg = "#062444")
        
        self.lb_ipServidor = tkinter.Label(self.frame_conexao, 
                                           text="IP:",
                                           font = self.fonte)
        
        self.entry_ipServidor = tkinter.Entry(self.frame_conexao,
                                              width = 14)
        
        self.lb_portaServidor = tkinter.Label(self.frame_conexao,
                                              text = "Porta:",
                                              font = self.fonte)
        
        self.entry_portaServidor = tkinter.Entry(self.frame_conexao,
                                                 width = 10)
        
        self.lb_statusConexaoServidor = tkinter.Label(self.frame_conexao,
                                              text = "Status:")
        
        # Label com status para indicar se a conexão com Servidor Central foi bem sucedida
        self.status_ConnServer = tkinter.Label(self.frame_conexao, 
                                            text = "Desconectado", fg = "red")
                
        self.lb_parametrosCliente = tkinter.Label(self.frame_conexao, 
                                                  text = "Parâmetros do Cliente", 
                                                  font = self.fonte, fg = "#062444")
        
        self.lb_ipCliente = tkinter.Label(self.frame_conexao,
                                          text = "IP:",
                                          font = self.fonte)
        
        self.entry_ipCliente = tkinter.Entry(self.frame_conexao,
                                              width = 14)
        
        # Captura o IP address do cliente
        hostname = gethostname()
        ipAddress_cliente = gethostbyname(hostname)
        
        # Insere como campo default, o IP address do cliente 
        self.entry_ipCliente.insert(0, ipAddress_cliente )
        
        self.lb_portaCliente = tkinter.Label(self.frame_conexao,
                                              text = "Porta:",
                                              font = self.fonte)
        
        self.entry_portaCliente = tkinter.Entry(self.frame_conexao,
                                                 width = 10)
        
        self.bt_conectar = tkinter.Button(self.frame_conexao,
                                          text = "Conectar",  fg = "white", bg = "gray",
                                          command = self.event_conectar)
        
        self.lb_statusModoPassivo = tkinter.Label(self.frame_conexao,
                                                text = "Modo passivo: ")
        
        # Label com status para indicar se o modo passivo do cliente foi ligado com sucesso
        self.status_ModoPassivo = tkinter.Label(self.frame_conexao, 
                                                     text = "OFF", fg = "red")
        
        # Posiciona os widgets no frame_conexao num grid (matriz)
        self.lb_parametrosServidor.grid(row = 0, column = 0, columnspan = 3)
        self.lb_ipServidor.grid(row = 1, column = 0 )
        self.entry_ipServidor.grid(row = 1, column = 1)
        self.lb_portaServidor.grid(row = 1, column = 2)
        self.entry_portaServidor.grid(row = 1, column = 3)
        self.lb_statusConexaoServidor.grid(row = 2, column = 0)
        self.status_ConnServer.grid(row = 2, column = 1)
        self.lb_parametrosCliente.grid(row = 3, column = 0, columnspan = 3)
        self.lb_ipCliente.grid(row = 4, column = 0)
        self.entry_ipCliente.grid(row = 4, column = 1)
        self.lb_portaCliente.grid(row = 4, column = 2)
        self.entry_portaCliente.grid(row = 4, column = 3)
        self.bt_conectar.grid(row = 4, column = 4)
        self.lb_statusModoPassivo.grid(row = 5, column = 0, columnspan = 1)
        self.status_ModoPassivo.grid(row = 5, column = 1)
        self.frame_conexao.pack()
    
    # Constroi o frame da GUI que lida com o input do nickname #
    def build_frameNickname(self):
        self.frame_nickname = tkinter.Frame(self.janela_root)

        # Constroi os widgets (elementos de janela) do frame
        self.lb_nickname = tkinter.Label(self.frame_nickname, 
                                         text = "Nickname:")
        
        self.entry_nickname = tkinter.Entry(self.frame_nickname, 
                                            width = 32)
        
        self.bt_setNickname = tkinter.Button(self.frame_nickname,
                                             text = "Set nick", fg = "white", bg = "gray",
                                             command = self.event_setNickname)
        
        self.lb_statusNickname = tkinter.Label(self.frame_nickname, text = "Cliente: ", fg = "gray")
        
        self.status_nickname = tkinter.Label(self.frame_nickname, text = "")
        
        # Posiciona os widgets no frame_nickname num grid (matriz)
        self.lb_nickname.grid(row = 0, column = 0, columnspan = 2)
        self.entry_nickname.grid(row = 0, column = 2)
        self.bt_setNickname.grid(row = 0, column = 3)
        self.lb_statusNickname.grid(row = 1, column = 0)
        self.status_nickname.grid(row = 1, column = 1, columnspan = 2)
        self.frame_nickname.pack()
    
    # Constroi o frame da GUI que lida com os inputs do chat (chatname e senha) #
    def build_frameChat(self):
        self.frame_chat = tkinter.Frame(self.janela_root)
        self.lb_parametrosChat = tkinter.Label(self.frame_chat, 
                                               text = "Parâmetros do Chat", fg = "#062444", font = self.fonte)
        self.lb_chatname = tkinter.Label(self.frame_chat, text = "Chatname:")
        self.entry_chatname = tkinter.Entry(self.frame_chat, width = 32)
        
        self.lb_senha_chat = tkinter.Label(self.frame_chat, text = "Senha: ")
        self.entry_senhaChatCriado = tkinter.Entry(self.frame_chat, width = 32)
        
        self.bt_criar_chat = tkinter.Button(self.frame_chat, text = "Criar chat", fg = "white", bg = "gray",
                                            command = self.event_criarChat)
        
        self.bt_atualizar_chat = tkinter.Button(self.frame_chat, text = "Atualizar", fg = "white", bg = "gray",
                                        command = self.event_atualizarChatsClientes)
        
        # Posiciona os widgets no frame_chat num grid (matriz)
        self.lb_parametrosChat.grid(row = 0, column = 0, columnspan = 3)
        self.lb_chatname.grid(row = 1, column = 0)
        self.entry_chatname.grid(row = 1, column = 1)
        self.bt_criar_chat.grid(row = 1, column = 2)
        self.lb_senha_chat.grid(row = 2, column = 0)
        self.entry_senhaChatCriado.grid(row = 2, column = 1)
        self.bt_atualizar_chat.grid(row = 2, column = 2)
        self.frame_chat.pack()
    
    # Constroi o frame da GUI que lista os clientes conectados e chats disponiveis 
    def build_frameClientes_Chats(self):
        self.frame_clientes_Chats = tkinter.Frame(self.janela_root)
        
        
        self.lb_clientesConectados = tkinter.Label(self.frame_clientes_Chats, 
                                                   text = "Clientes Conectados")
        
        self.ltb_clientesConectados = tkinter.Listbox(self.frame_clientes_Chats)
        
        
        self.lb_chatsDisponiveis = tkinter.Label(self.frame_clientes_Chats,
                                                 text = "Chats Disponíveis")
        
        self.ltb_chatsDisponiveis = tkinter.Listbox(self.frame_clientes_Chats)
        
        self.bt_entrarChat = tkinter.Button(self.frame_clientes_Chats, text = "Entrar chat", 
                                            fg = "white", bg = "gray", command = self.event_entrarChat)
        
        self.entry_senhaChat = tkinter.Entry(self.frame_clientes_Chats, fg = "#092366")
        self.entry_senhaChat.insert(0, "(senha)")
        
        
        self.lb_statusEntrarChat = tkinter.Label(self.frame_clientes_Chats, text = "")
        
        # Posiciona os widgets no frame_clientes_Chats        
        self.lb_clientesConectados.grid(row = 0, column = 0)
        self.lb_chatsDisponiveis.grid(row = 0, column = 1)
        self.ltb_clientesConectados.grid(row = 1, column = 0)
        self.ltb_chatsDisponiveis.grid(row = 1, column = 1)
        self.entry_senhaChat.grid(row = 2, column = 1)
        self.bt_entrarChat.grid(row = 2, column = 2, columnspan = 2)
        self.lb_statusEntrarChat.grid(row = 3, column = 1, columnspan = 2)
        self.frame_clientes_Chats.pack()
        
    # Eventos acionados na GUI
    
    # Evento do botão conectar no frame_conexao #
    def event_conectar(self):
        # Captura o texto nos campos entries
        ip_servidor = self.entry_ipServidor.get()
        porta_servidor = self.entry_portaServidor.get()
        ip_cliente = self.entry_ipCliente.get()
        porta_cliente = self.entry_portaCliente.get()
        
        # Cria um objeto cliente uma única vez
        if not self.existe_cliente_GUI:
            self.cliente = Cliente(ip_cliente, porta_cliente, ip_servidor, porta_servidor)
            self.existe_cliente_GUI = True
  
        # Se o ip_cliente e porta_cliente forem vazios, não deixa conectar
        if ip_cliente == "" or porta_cliente == "":
            return
  
        # Atualiza os campos desse cliente com os valores passados na GUI (Set direto)
        self.cliente.ip_cliente = ip_cliente
        self.cliente.porta_cliente = porta_cliente
        self.cliente.ip_servidor = ip_servidor
        self.cliente.porta_servidor = porta_servidor
        
        # Se a chave da thread do Servidor Cliente está aberta, então feche-a 
        if not self.chave_thread_servidorCliente:
            self.chave_thread_servidorCliente = True
            thread_servidorCliente = threading.Thread(target = self.cliente._init_modoPassivo)
            thread_servidorCliente.start()
            sleep(0.1)    # Coloca a main thread para dormir por 0.1 ms => Switch para thread lançada
                
        # Verifica se o cliente qualquer está no modo passivo
        if self.cliente.isModoPassivo:
            # Mude os Status da GUI do modo passivo
            self.entry_ipCliente.config(state = "disabled")
            self.entry_portaCliente.config(state = "disabled")
            self.status_ModoPassivo.config(text = "ON", fg = "#092366")
        else:
            self.chave_thread_servidorCliente = False
            self.existe_cliente_GUI = False
            return
        
        # Verifica a conexão do cliente com Servidor central
        if self.cliente._init_conexaoServidor():
            # Mude os Status da GUI do Servidor Central
            self.entry_ipServidor.config(state = "disabled")
            self.entry_portaServidor.config(state = "disabled")
            self.status_ConnServer.config(text = "Conectado", fg = "#092366")
            self.isConectadoServidor = True
                      
    # Evento no botão set nick no frame_nickname # 
    def event_setNickname(self):
        # Captura o nickname digitado
        nickname = self.entry_nickname.get()
        if nickname == "":
            return
        if self.isConectadoServidor:
            # Assim que está conectado ao Servidor e tenta setar o nickname, atualiza os chats e os clientes ON
            self.event_atualizarChatsClientes()
            if not self.cli_nickname:
                if self.cliente.setNickname(nickname):
                    self.cli_nickname = nickname
                    self.entry_nickname.config(state = "disabled")
                    self.lb_statusNickname.config(fg = "black")
                    self.status_nickname.config(text = nickname, fg = "#092366")
                    self.event_atualizarChatsClientes()
                else:
                    self.status_nickname.config(text = "Nome já utilizado! Escolha outro", fg = "red")
        else:
            self.status_nickname.config(text = "Conecte com Servidor", fg = "red")
    
    # Evento no botão criar chat no frame_chat #
    def event_criarChat(self):
        # Captura o chatname e a senha digitados
        chatname = self.entry_chatname.get()
        senha = self.entry_senhaChatCriado.get()
        if chatname == "":
            return
        if senha == "":
            senha = False
        if self.isConectadoServidor and self.cli_nickname:
            self.cliente.criarChat(chatname, senha)
            self.entry_chatname.delete(0, "end")
            self.entry_senhaChatCriado.delete(0, "end")
            self.event_atualizarChatsClientes()
            
            # Se conectado com servidor, seta o status novamente para sua configuração normal    
            self.lb_statusEntrarChat.config(text = "")
        else:
            # Uso da label de status de entrada no chat para setar um warning quanto a criação do chat
            self.lb_statusEntrarChat.config(text = "Conecte no Servidor e sete um nick!", fg = "red")

    # Evento de atualizar os clientes conectados e os chats disponiveis
    def event_atualizarChatsClientes(self):
        if self.isConectadoServidor:
            # Atualiza todos os chats disponiveis
            
            # Remove todos os itens do listbox de chats disponíveis
            self.ltb_chatsDisponiveis.delete(0, "end")
            # Acrescenta os chats Disponíveis no Servidor nesse listbox
            chatsDisponiveis = self.cliente.verChatsDisponiveis() 
            chat_number = 0
            for chat in chatsDisponiveis:
                dados_chat = self.cliente.verificarDadosChat(chat)
                # Se o chat tiver senha, coloque-o no listbox com uma formatação diferente 
                if dados_chat["senha"]:
                    self.ltb_chatsDisponiveis.insert(chat_number, chat + " (priv) ")
                    self.ltb_chatsDisponiveis.itemconfig(chat_number, foreground = "#092366")
                else:
                    self.ltb_chatsDisponiveis.insert(chat_number, chat)
                chat_number += 1
        
            # Atualiza todos os clientes conectados
            
            # Remove todos os itens do listbox de clientes conectados
            self.ltb_clientesConectados.delete(0, "end")
            # Acrescenta os clientes conectados no Servidor nesse listbox
            clientesConectados = self.cliente.verClientesConectados()
            cliente_number = 0
            for cliente in clientesConectados:
                self.ltb_clientesConectados.insert(cliente_number, cliente)
                # Se o cliente for o cliente da GUI, então coloque-o no listbox com uma formatação diferente
                if cliente == self.cli_nickname:
                    self.ltb_clientesConectados.itemconfig(cliente_number, foreground = "#092366")
                cliente_number += 1
            
            # Se conectado com servidor, seta o status novamente para sua configuração normal
            self.lb_statusEntrarChat.config(text = "")
        else:
            # Uso da label de status de entrada do chat para setar um warning quanto atualização dos clientes e chats
            self.lb_statusEntrarChat.config(text = "Conecte com o Servidor!", fg = "red")
            

    # Evento no botão entrar no frame_clientes_Chats
    def event_entrarChat(self):
        if self.isConectadoServidor and self.cli_nickname:
            # Seleciona um chat do listbox
            chatSelecionado = self.ltb_chatsDisponiveis.get(tkinter.ACTIVE)
            # Verifica se tal chat tem a substring ( priv ), i.e, tal chat contêm senha
            posSubstring_priv = chatSelecionado.find(" (priv) ")
            # Se tiver, então remove essa substring do nome do chat
            if posSubstring_priv > 0:
                chatSelecionado = chatSelecionado[:posSubstring_priv]
            # Captura a senha digitada
            senhaDigitada = self.entry_senhaChat.get()
            # Se nenhuma senha for passada ou a senha digitada seja a default = (senha), então sete False
            if senhaDigitada == "" or senhaDigitada == "(senha)":
                senhaDigitada = False
            
            # Se não foi aberto uma janela de chat para esse chat selecionado, então abra (instância ChatWindow)
            if chatSelecionado not in self.janelasChat:
                if self.cliente.entrarChat(chatSelecionado, senhaDigitada):
                    self.lb_statusEntrarChat.config(text = "")
                    self.entry_senhaChat.delete(0, "end")
                    root_chat = tkinter.Tk()
                    chatWindow = ChatWindow(root_chat, chatSelecionado, self.cliente)
                    MainWindow.janelasChat[chatSelecionado] = [root_chat, chatWindow]
                    root_chat.mainloop() # Mainloop encerrou
                else:
                    self.lb_statusEntrarChat.config(text = "Senha incorreta!", fg = "red")
        else:
            self.lb_statusEntrarChat.config(text = "Conecte no Servidor e sete um nick!", fg = "red")
                
    # Destroi a janela principal, encerrando as conexões do cliente (modo passivo, servidor central)
    # e as salas de chat abertas (gerenciadas pela MainWindow)
    def _destroy_janela_root(self):
        # Se o cliente está na GUI, desliga suas conexões (modo passivo e servidor central)
        if self.existe_cliente_GUI:
            # Se está no modo passivo
            if self.cliente.isModoPassivo:
                self.cliente._destroy_modoPassivo()
            # Se o cliente está conectado ao Servidor e seu nickname foi setado, desregistre-o do Servidor
            if self.isConectadoServidor and self.cli_nickname:
                # Mas antes, se existem janelas de chat abertas, feche-as antes de destruir a conexão com Servidor
                janelasChatAbertas = MainWindow.janelasChat
                if janelasChatAbertas:
                    for janela in janelasChatAbertas:
                        list_chatObject = janelasChatAbertas.get(janela)
                        root_chat, chatWindow = list_chatObject[0], list_chatObject[1]
                        chatWindow.cliente.sairChat(janela)
                        root_chat.destroy()
                # Destroi a conexão com servidor
                self.cliente._destroy_conexaoServidor()
        # Destroi a MainWindow da GUI
        self.janela_root.destroy()

class ChatWindow:
    ''' Classe que representa as janelas de chat abertas na GUI '''
    
    def __init__(self, master, chatname, cliente):
        self.janela_chat = master
        # Variáveis relativas ao chat e ao cliente
        self.chatname = chatname
        self.cliente = cliente
        
        dados_chat = self.cliente.verificarDadosChat(chatname)
        self.clientOwner = dados_chat["criador"]
        self.senha = dados_chat["senha"]
        
        # Armazena a ultima mensagem recebida no chat
        self.lastMessage = "" 
        
        # Parâmetros da janela de chat
        self.titulo = "< Chat: " + chatname + " >"
        self.janela_chat.title(self.titulo)
        self.janela_chat.geometry("600x520")
        self.janela_chat.resizable(0,0)
        
        # Protocolo de destruição da janela da GUI. Assim que X é pressionado 
        # chama o método: _destroy_chatWindow
        master.protocol("WM_DELETE_WINDOW", self._destroy_chatWindow)
                
        # Frames
        self.build_frameMembros()
        self.build_frameChat()
        
    # Constroi o frame que contêm os membros do chat
    def build_frameMembros(self):
        self.frame_membros = tkinter.Frame(self.janela_chat)
        self.lb_membrosChat = tkinter.Label(self.frame_membros, text = "< Membros do Chat > ", fg = "#092366")
        self.ltb_membrosChat = tkinter.Listbox(self.frame_membros, bg = "#f9feff")  # essa cor é um azul claro
        self.ltb_membrosChat.configure(height = 30, width = 20)
        
        # Posicionando os widgets
        self.lb_membrosChat.grid(row = 0, column = 0)
        self.ltb_membrosChat.grid(row = 1, column = 0)
                
        self.frame_membros.pack(side = "left")

    # Constroi o frame do chat
    def build_frameChat(self):
        self.frame_chat = tkinter.Frame(self.janela_chat)
        self.lb_chat = tkinter.Label(self.frame_chat, text = "< Chat: " + self.chatname + " - Criador: " + 
                                     self.clientOwner + " >", fg = "#092366" )
        
        self.txt_chat = tkinter.Text(self.frame_chat, state = "disabled")
        self.txt_chat.configure(height = 25, width = 60)
        
        # Constroi o frame que agrupa os botões (historico, video e sair) dentro do frame do chat
        self.frame_buttons = tkinter.Frame(self.frame_chat)
        # Constroi os botões
        self.bt_historicoMSG = tkinter.Button(self.frame_buttons, text = "Historico", fg = "white", bg = "gray")
        self.bt_transmissaoVideo = tkinter.Button(self.frame_buttons, text = "Video", fg = "white", bg = "gray")
        self.bt_sairChat = tkinter.Button(self.frame_buttons, text = "Sair", fg = "white", bg = "gray", 
                                          command = self._destroy_chatWindow)
        
        # Constroi o frame para entrada de mensagem dentro do frame do chat 
        self.frame_mensagem = tkinter.Frame(self.frame_chat)
        self.entry_mensagem = tkinter.Entry(self.frame_mensagem)
        self.entry_mensagem.configure(width = 37)
        self.entry_mensagem.bind('<Return>', self.enviarMensagem)
        self.bt_enviar = tkinter.Button(self.frame_mensagem, text = "Enviar", bg = "gray", fg = "#0e3a5e")
        self.bt_enviar.bind('<Button-1>', self.enviarMensagem)
        
        # Posicionando os widgets
        self.lb_chat.pack()
        self.txt_chat.pack()
        
        # Posiciona os botões
        self.bt_historicoMSG.grid(row = 0, column = 0)
        self.bt_transmissaoVideo.grid(row = 0, column = 1)
        self.bt_sairChat.grid(row = 0, column = 2)
        
        # Posiciona o campo para entrada de mensagem
        self.entry_mensagem.pack(side = "left")
        self.bt_enviar.pack(side = "left")
        
        # Posiciona os frames
        self.frame_buttons.pack()
        self.frame_mensagem.pack()
        self.frame_chat.pack()
        
        # Lança uma thread, uma única vez, para receber mensagens
        self.txt_chat.after(1000, self.verificarMensagem)

    # Verifica se houve mensagem enviada para esse cliente por algum outro membro do chat
    def verificarMensagem(self):
        # Toda vez que atualiza mensagens, atualiza os membros também
        self.atualizarMembros()
        lastMessage = self.cliente.verMensagemRecebida(self.chatname)
        # Se a última mensagem for diferente da última anterior, então mostre a última
        if lastMessage != self.lastMessage:
            self.txt_chat.config(state = "normal")
            self.txt_chat.insert("end", lastMessage)
            self.txt_chat.config(state = "disabled")
            self.lastMessage = lastMessage
        
        # A cada 1s verifica se a última mensagem enviada no chat foi alterada
        self.txt_chat.after(1000, self.verificarMensagem)
        
    # Atualiza o listbox de membros do chat
    def atualizarMembros(self):
        membrosChat = self.cliente.verMembrosChat(self.chatname)
        # Remove todos os itens do listbox de chats disponíveis
        self.ltb_membrosChat.delete(0, "end")
        membroNumber = 0
        for membro in membrosChat:
            self.ltb_membrosChat.insert(membroNumber, membro)
            if membro == self.cliente.nickname:
                self.ltb_membrosChat.itemconfig(membroNumber, foreground = "#092366")
            membroNumber += 1
    
    # Event handler para enviar a mensagem
    def enviarMensagem(self, event):
        mensagem = self.entry_mensagem.get()
        self.txt_chat.config(state = "normal")
        self.txt_chat.insert("end", "Você diz: " + mensagem + '\n')
        self.txt_chat.config(state = "disabled")
        self.lastMessage = self.cliente.nickname + " diz: " + mensagem + '\n'
        self.cliente.compartilharMsg(mensagem, self.chatname)
        self.entry_mensagem.delete(0, "end")        
    
    # Destroi a janela de chat
    def _destroy_chatWindow(self):
        self.cliente.sairChat(self.chatname)
        MainWindow.janelasChat.pop(self.chatname)
        self.janela_chat.destroy()
        
def main():
    # Cria a janela raiz da GUI, interpretada via TCL
    root = tkinter.Tk()
    # Instância a janela principal da GUI com a janela root (raiz)
    GUI = MainWindow(root)
    # Mantêm a janela raiz em loop eterno até ser fechada
    root.mainloop()

if __name__ == "__main__":
    main()
    
