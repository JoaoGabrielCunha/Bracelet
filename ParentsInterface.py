import tkinter as tk
from tkinter import font
import tkintermapview
import json
import time

janela = tk.Tk()
janela.title("Interface dos pais")
janela.geometry("900x550")


global emoji_list
emoji_list =[{'nome':'ok','simbolo':'👍'},{'nome':'not_ok','simbolo':'👎'},{'nome':'aparelho_auditivo','simbolo':'🦻'},{'nome':'banho','simbolo':'🛀'},{'nome':'dormir','simbolo':'🛌'},{'nome':'comida','simbolo':'🍽'},{'nome':'bola','simbolo':'⚽'},{'nome':'casa','simbolo':'🏡'},{'nome':'onibus','simbolo':'🚍'},{'nome':'carro','simbolo':'🚔'},{'nome':'chuva','simbolo':'🌧'},{'nome':'guarda_chuva','simbolo':'☂'},{'nome':'telefone','simbolo':'📞'}]

def selecionar_emoji(emoji_selecionado):
    mensagem_atual = msg.get()
    nova_mensagem = mensagem_atual + emoji_selecionado
    msg.set(nova_mensagem)

# Campo de mensagem
etiqueta_msg = tk.Label(janela, text="Enviar mensagem: ", font=font.Font(size=10, weight="bold"))
etiqueta_msg.place(x=20, y=15)

msg = tk.StringVar() # guardar o texto digitado pelo usuário
campo_msg = tk.Entry(janela, width=55, textvariable=msg)
campo_msg.place(x=22, y=45)

# Emoji na mensagem
emoji_var = tk.StringVar(value="🙂")
opcoes_emoji = [emoji["simbolo"] for emoji in emoji_list]
campo_emoji = tk.OptionMenu(janela, emoji_var, *opcoes_emoji, command=selecionar_emoji)
campo_emoji.config(width=1)
campo_emoji.pack(pady=20)
campo_emoji.place(x=370, y=38)

def enviar_mensagem():
    mensagem = msg.get()  # Obtém a mensagem atual
    print(mensagem)
    campo_msg.delete(0, tk.END)

botao_enviar = tk.Button(janela, text="Enviar", command = enviar_mensagem, bg="green", width = 10)
botao_enviar.place(x=435,y=40)

################################################
# Botões de mensagem pré-programados
################################################

etiqueta_msg = tk.Label(janela, text="Mensagens pré-programadas:", font=font.Font(size=10,weight="bold"))
etiqueta_msg.place(x=20, y=80)

def obter_nome_emoji(emoji_selecionado):
    global emoji_list
    for emoji in emoji_list:
        if emoji["simbolo"] == emoji_selecionado:
            return emoji["nome"]
    return None

def salvar_alteracoes():
    # Atualiza a lista msg_alterada com os valores atuais dos campos de entrada
    msg_alterada[0] = msg1.get()
    msg_alterada[1] = msg2.get()
    msg_alterada[2] = msg3.get()
    msg_alterada[3] = msg4.get()
   
    emojis_salvos.append(obter_nome_emoji(emoji_var1.get()))
    emojis_salvos.append(obter_nome_emoji(emoji_var2.get()))
    emojis_salvos.append(obter_nome_emoji(emoji_var3.get()))
    emojis_salvos.append(obter_nome_emoji(emoji_var4.get()))

    # Salva a lista msg_alterada em um arquivo JSON
    with open("mensagens_alteradas.json", "w") as arquivo:
        json.dump(msg_alterada, arquivo, indent=4)

    # Salva a lista emojis_salvos em um arquivo JSON
    with open("emojis_salvos.json", "w") as arquivo:
        json.dump(emojis_salvos, arquivo, indent=4)

    janela2.destroy()  # Fecha a janela após salvar as alterações

def cancelar_alteracoes():
    janela2.destroy()

def imprimir_json():
    with open("mensagens_alteradas.json", "r") as arquivo:
        dados = json.load(arquivo)
        print("Conteúdo do JSON:", dados)
    with open("emojis_salvos.json", "r") as arquivo2:
        dados2 = json.load(arquivo2)
        print("Emojis Salvos: ", dados2)
#imprimir_json()



# Função para abrir a janela de alteração de mensagens
def alterar_msg_programada():
    global janela2, msg1, msg2, msg3, msg4, msg_alterada, emojis_salvos, emoji_list, emoji_var1, emoji_var2, emoji_var3, emoji_var4
   
    msg_alterada = ["", "", "", ""]  # Inicializa a lista de mensagens alteradas

    janela2 = tk.Toplevel()
    janela2.title("Alterar mensagens pré-programadas")
    janela2.geometry("500x250")
    emojis_salvos = []

    # Ler mensagens salvas do arquivo JSON
    msg_alterada = mensagens_json("mensagens_alteradas.json", "M")
    emojis_salvos = mensagens_json("emojis_salvos.json", "E")
#    print(emojis_salvos)
#    print(msg_alterada)
    # Mensagem 1
    etiqueta_msg1 = tk.Label(janela2, text="Alterar mensagem 1: ")
    etiqueta_msg1.place(x=20, y=20)
    msg1 = tk.StringVar(value=msg_alterada[0])
    campo_msg1 = tk.Entry(janela2, width=30, textvariable=msg1)
    campo_msg1.place(x=22, y=45)
    # Dropdown 1
    emoji_var1 = tk.StringVar(value=obter_simbolo_emoji(emojis_salvos[-4]))
    opcoes_emoji = [emoji["simbolo"] for emoji in emoji_list]
    campo_emoji1 = tk.OptionMenu(janela2, emoji_var1, *opcoes_emoji)
    campo_emoji1.config(width=8)
    campo_emoji1.pack(pady=20)
    campo_emoji1.place(x=210, y=38)


    # Mensagem 2
    etiqueta_msg2 = tk.Label(janela2, text="Alterar mensagem 2: ")
    etiqueta_msg2.place(x=20, y=70)
    msg2 = tk.StringVar(value=msg_alterada[1])
    campo_msg2 = tk.Entry(janela2, width=30, textvariable=msg2)
    campo_msg2.place(x=22, y=95)
    # Dropdown 2
    emoji_var2 = tk.StringVar(value=obter_simbolo_emoji(emojis_salvos[-3]))
    opcoes_emoji = [emoji["simbolo"] for emoji in emoji_list]
    campo_emoji2 = tk.OptionMenu(janela2, emoji_var2, *opcoes_emoji)
    campo_emoji2.config(width=8)
    campo_emoji2.pack(pady=20)
    campo_emoji2.place(x=210, y=88)


    # Mensagem 3
    etiqueta_msg3 = tk.Label(janela2, text="Alterar mensagem 3: ")
    etiqueta_msg3.place(x=20, y=120)
    msg3 = tk.StringVar(value=msg_alterada[2])
    campo_msg3 = tk.Entry(janela2, width=30, textvariable=msg3)
    campo_msg3.place(x=22, y=145)
    # Dropdown 3
    emoji_var3 = tk.StringVar(value=obter_simbolo_emoji(emojis_salvos[-2]))
    opcoes_emoji = [emoji["simbolo"] for emoji in emoji_list]
    campo_emoji3 = tk.OptionMenu(janela2, emoji_var3, *opcoes_emoji)
    campo_emoji3.config(width=8)
    campo_emoji3.pack(pady=20)
    campo_emoji3.place(x=210, y=138)
   

    # Mensagem 4
    etiqueta_msg4 = tk.Label(janela2, text="Alterar mensagem 4: ")
    etiqueta_msg4.place(x=20, y=170)
    msg4 = tk.StringVar(value=msg_alterada[3])
    campo_msg4 = tk.Entry(janela2, width=30, textvariable=msg4)
    campo_msg4.place(x=22, y=195)
    # Dropdown 4
    emoji_var4 = tk.StringVar(value=obter_simbolo_emoji(emojis_salvos[-1]))
    opcoes_emoji = [emoji["simbolo"] for emoji in emoji_list]
    campo_emoji4 = tk.OptionMenu(janela2, emoji_var4, *opcoes_emoji)
    campo_emoji4.config(width=8)
    campo_emoji4.pack(pady=20)
    campo_emoji4.place(x=210, y=190)
   
   
    botao_cancelar = tk.Button(janela2, text = "       Cancelar       ", command = cancelar_alteracoes, bg="red")
    botao_cancelar.place(x=350, y=160)
   
    botao_salvar = tk.Button(janela2, text = "Salvar alterações", command = salvar_alteracoes, bg="green")
    botao_salvar.place(x=350, y=200)

botao_alterar_msg_programada = tk.Button(janela, text="...", command = alterar_msg_programada)
botao_alterar_msg_programada.place(x=225, y = 80)

def obter_simbolo_emoji(nome_emoji):
    global emoji_list
    for emoji in emoji_list:
        if emoji["nome"] == nome_emoji:
            return emoji["simbolo"]
    return "(selecione)"

def funcao_botao1():
    with open("mensagens_alteradas.json", "r") as arquivo1:
        dados1 = json.load(arquivo1)
        print(dados1[0])
       
    with open("emojis_salvos.json", "r") as arquivo2:
        dados2 = json.load(arquivo2)
        nome_emoji = dados2[-4]  # Supondo que o arquivo emojis_salvos.json contenha uma lista de nomes de emojis
        simbolo_correspondente = obter_simbolo_emoji(nome_emoji)
        if simbolo_correspondente:
            print(simbolo_correspondente)
        else:
            print(nome_emoji)
def funcao_botao2():
    with open("mensagens_alteradas.json", "r") as arquivo1:
        dados1 = json.load(arquivo1)
        print(dados1[1])
       
    with open("emojis_salvos.json", "r") as arquivo2:
        dados2 = json.load(arquivo2)
        nome_emoji = dados2[-3]  # Supondo que o arquivo emojis_salvos.json contenha uma lista de nomes de emojis
        simbolo_correspondente = obter_simbolo_emoji(nome_emoji)
        if simbolo_correspondente:
            print(simbolo_correspondente)
        else:
            print(nome_emoji)
def funcao_botao3():
    with open("mensagens_alteradas.json", "r") as arquivo1:
        dados1 = json.load(arquivo1)
        print(dados1[2])
       
    with open("emojis_salvos.json", "r") as arquivo2:
        dados2 = json.load(arquivo2)
        nome_emoji = dados2[-2]  # Supondo que o arquivo emojis_salvos.json contenha uma lista de nomes de emojis
        simbolo_correspondente = obter_simbolo_emoji(nome_emoji)
        if simbolo_correspondente:
            print(simbolo_correspondente)
        else:
            print(nome_emoji)
def funcao_botao4():
    with open("mensagens_alteradas.json", "r") as arquivo1:
        dados1 = json.load(arquivo1)
        print(dados1[3])
       
    with open("emojis_salvos.json", "r") as arquivo2:
        dados2 = json.load(arquivo2)
        nome_emoji = dados2[-1]  # Supondo que o arquivo emojis_salvos.json contenha uma lista de nomes de emojis
        simbolo_correspondente = obter_simbolo_emoji(nome_emoji)
        if simbolo_correspondente:
            print(simbolo_correspondente)
        else:
            print(nome_emoji)

def mensagens_json(arquivo_json, MoE):
    try:
        with open(arquivo_json, "r") as arquivo:
            mensagens = json.load(arquivo)
    except FileNotFoundError:
        # Se o arquivo não existir, usar mensagens padrão
        if(MoE == "M"):
            mensagens = ["Botão 1", "Botão 2", "Botão 3", "Botão 4"]
        if(MoE == "E"):
            mensagens = ["(selecione)","(selecione)","(selecione)","(selecione)"]
    return mensagens

mensagens = mensagens_json("mensagens_alteradas.json","M")
emojis = (mensagens_json("emojis_salvos.json","E")[-4:])
simbolos = []
for emoji in emojis:
    simbolos.append(obter_simbolo_emoji(emoji))

# Função para calcular a posição x dos botões
def calcular_posicoes_botoes(mensagens):
    pos_x = []
    x_atual = 20
    for mensagem in mensagens:
        pos_x.append(x_atual)
        largura_botao = tk.Button(janela, text=mensagem).winfo_reqwidth()
        x_atual += largura_botao + 20  # 20 pixels de espaçamento entre os botões
    return pos_x

pos_x = calcular_posicoes_botoes(mensagens)


botao1 = tk.Button(janela, text=mensagens[0], command = funcao_botao1, fg = "red")
botao1.place(x=pos_x[0], y=110)
emoji1 = tk.Label(janela, text=simbolos[0])
emoji1.place(x=pos_x[0], y=140)
   
botao2 = tk.Button(janela, text=mensagens[1], command = funcao_botao2, fg = "red")
botao2.place(x=pos_x[1], y=110)
emoji2 = tk.Label(janela, text=simbolos[1])
emoji2.place(x=pos_x[1], y=140)

botao3 = tk.Button(janela, text=mensagens[2], command = funcao_botao3, fg = "red")
botao3.place(x=pos_x[2], y=110)
emoji3 = tk.Label(janela, text=simbolos[2])
emoji3.place(x=pos_x[2], y=140)
   
botao4 = tk.Button(janela, text=mensagens[3], command = funcao_botao4, fg = "red")
botao4.place(x=pos_x[3], y=110)
emoji4 = tk.Label(janela, text=simbolos[3])
emoji4.place(x=pos_x[3], y=140)

#################################################################################################
#################################################################################################
#################################################################################################

# Alerta

def display_de_alerta(msg):
    if msg != "" and msg != None:
        etiqueta_alerta = tk.Label(janela, text="Mensagem de alerta:", font=font.Font(size=10,weight="bold"))
        etiqueta_alerta.place(x=600, y=20)
        
        msg_alerta = tk.Label(janela, text=msg, font=font.Font(size=15,weight="bold"), fg = "red")
        msg_alerta.place(x=620, y=40)

display_de_alerta("Help!")


#################################################################################################
#################################################################################################
#################################################################################################

# Localização
etiqueta_localizacao = tk.Label(janela, text="Localização: ", font=font.Font(size=10,weight="bold"))
etiqueta_localizacao.place(x=20, y=240)

map_widget = tkintermapview.TkinterMapView(janela, width=550, height=250, corner_radius=1)
map_widget.place(x=300, y=250)
map_widget.set_position(-22.980039, -43.231579)  # PUC-rio, Brazil
map_widget.set_zoom(18)

def imprimir_conteudo_json():
    try:
        with open("localizacao.json", "r") as arquivo:
            dados = json.load(arquivo)
        print("Conteúdo do arquivo JSON:")
        print(dados)
    except FileNotFoundError:
        print("O arquivo JSON não foi encontrado.")

# Inicializa as variáveis globais
global marker_loc
marker_loc = None
posicoes = [(-22.980039, -43.231579),(-22.981500, -43.232000),(-22.982000, -43.233000),(-22.983000, -43.234000),(-22.984000, -43.235000),(-22.985000, -43.236000),(-22.986000, -43.237000),(-22.987000, -43.238000),(-22.988000, -43.239000),(-22.989000, -43.240000),(-22.990000, -43.241000),(-22.991000, -43.242000),(-22.992000, -43.243000),(-22.993000, -43.244000),(-22.994000, -43.245000),(-22.995000, -43.246000),(-22.996000, -43.247000),(-22.997000, -43.248000),(-22.998000, -43.249000),(-22.999000, -43.250000)]

posicao_atual = 0

# Função para salvar os dados no arquivo JSON
def salvar_localizacao(x, y, timestamp):
    try:
        # Tenta abrir o arquivo em modo de leitura
        with open("localizacao.json", "r") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        # Se o arquivo não existir, inicializa com uma lista vazia
        dados = []

    # Adiciona o novo ping
    dados.append({"data": timestamp, "x": x, "y": y})

    # Mantém apenas os últimos 10 pings
    if len(dados) > 9:
        dados = dados[-9:]  # Remove o primeiro elemento da lista

    # Salva os dados de volta no arquivo
    with open("localizacao.json", "w") as arquivo:
        json.dump(dados, arquivo, indent=4)
# Função para pingar a localização
def pinga_localizacao():
    global marker_loc, posicao_atual
    if marker_loc != None:
        marker_loc.delete()
   
    x, y = posicoes[posicao_atual]
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    marker_loc = map_widget.set_marker(x, y, text=f"Localização atual\n{timestamp}")
   
    # Salva a localização no arquivo JSON
    salvar_localizacao(x, y, timestamp)
    posicao_atual = (posicao_atual + 1) % len(posicoes)
   
    imprimir_conteudo_json()
    janela.after(10000, pinga_localizacao)  # Atualiza após 20 segundos

# Inicia a primeira atualização
pinga_localizacao()


def mostrar_loc_anteriores():
    # Altera o texto do botão
    if botao_loc.cget("text") == "Mostrar localizações anteriores":
        with open("localizacao.json", "r") as arquivo:
            dados = json.load(arquivo)
        for ponto in dados:
            map_widget.set_marker(ponto["x"], ponto["y"], text=ponto["data"],marker_color_outside="blue",marker_color_circle="dark blue")
        botao_loc.config(text="Apagar localizações anteriores")
    else:
        map_widget.delete_all_marker()
        botao_loc.config(text="Mostrar localizações anteriores")
        with open("localizacao.json", "r") as arquivo:
            dados = json.load(arquivo)
            map_widget.set_marker(dados[-1]["x"], dados[-1]["y"], text=dados[-1]["data"])


botao_loc = tk.Button(janela, text="Mostrar localizações anteriores", command=mostrar_loc_anteriores)
botao_loc.place(x=20, y=300)







janela.mainloop()
