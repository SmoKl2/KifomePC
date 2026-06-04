import tkinter as tk
from PIL import Image, ImageTk
import Menu
import Carrinho
import Configuracoes
import sys
import os
import sqlite3
import ctypes

myappid = 'kifome.app.v1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def pasta_app():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.abspath(".")

def montar_tela(frame, voltar, janela_principal):
    for widget in frame.winfo_children():
        widget.destroy()

    # --- SISTEMA DE TEMAS - SÓ LÊ O ESTADO ---
    if not hasattr(janela_principal, 'tema_escuro'):
        janela_principal.tema_escuro = False

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

    temas = {
        "claro": {
            "fundo": "#FCB57D",
            "texto": "#2c3e50",
            "rodape": "white",
            "texto_rodape": "Black"
        },
        "escuro": {
            "fundo": "#1e272e",
            "texto": "#ecf0f1",
            "rodape": "#0f1419",
            "texto_rodape": "#ecf0f1"
        }
    }

    def pegar_cor(chave):
        tema_atual = "escuro" if janela_principal.tema_escuro else "claro"
        return temas[tema_atual][chave]

    cor_fundo = pegar_cor("fundo")
    frame.config(bg=cor_fundo)

    # Tamanho da Tela
    largura_tela = janela_principal.winfo_screenwidth()
    altura_tela = janela_principal.winfo_screenheight()

    def voltar_pro_menu():
        montar_tela(frame, voltar_pro_menu, janela_principal)

    # Banco
    conn = sqlite3.connect(os.path.join(pasta_app(), "cardapio.db"))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            preco REAL,
            descricao TEXT,
            imagem TEXT
        )
    """)
    conn.commit()

    # Logo Kifome
    caminho_imagem = resource_path(r"Imagens\nome kifome.png")
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            largura_logo = int(largura_tela * 0.45)
            altura_logo = int(largura_logo * 0.367)
            img_original = img_original.resize((largura_logo, altura_logo))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame, image=img_tk, bg=cor_fundo)
            label_img.pack(pady=(altura_tela * 0.02, 0))
        except:
            pass

    # Tamanho dos Botões
    largura_botao = int(largura_tela * 0.28)
    altura_botao = int(altura_tela * 0.45)

    # Botão Menu
    def abrir_menu():
        for widget in frame.winfo_children():
            widget.destroy()
        Menu.montar_tela(frame, voltar_pro_menu, janela_principal)

    imagem_original = Image.open(resource_path(r"Imagens\Menu.png"))
    imagem_original = imagem_original.resize((largura_botao, altura_botao))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao_menu = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_menu,
        borderwidth=0,
        highlightthickness=0,
        bg=cor_fundo,
        activebackground=cor_fundo,
        relief="flat",
        cursor="hand2",
    )
    botao_menu.place(relx=0.17, rely=0.6, anchor="center")

    # Botão Carrinho
    def abrir_carrinho():
        for widget in frame.winfo_children():
            widget.destroy()
        Carrinho.montar_tela(frame, voltar_pro_menu, janela_principal)

    imagem_original = Image.open(resource_path(r"Imagens\Carrinho.png"))
    imagem_original = imagem_original.resize((largura_botao, altura_botao))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao_carrinho = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_carrinho,
        borderwidth=0,
        highlightthickness=0,
        bg=cor_fundo,
        activebackground=cor_fundo,
        relief="flat",
        cursor="hand2",
    )
    botao_carrinho.place(relx=0.497, rely=0.6, anchor="center")

    # Botão Configurações
    def abrir_config():
        for widget in frame.winfo_children():
            widget.destroy()
        Configuracoes.montar_tela(frame, voltar_pro_menu, janela_principal)

    imagem_original = Image.open(resource_path(r"Imagens\Configurações.png"))
    imagem_original = imagem_original.resize((largura_botao, altura_botao))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao_config = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_config,
        borderwidth=0,
        highlightthickness=0,
        bg=cor_fundo,
        activebackground=cor_fundo,
        relief="flat",
        cursor="hand2",
    )
    botao_config.place(relx=0.825, rely=0.6, anchor="center")

    # Altura janela
    altura_tela = janela_principal.winfo_height()
    if altura_tela <= 1:
        altura_tela = janela_principal.winfo_screenheight()

    # Rodapé
    altura_rodape = int(altura_tela * 0.07)
    rodape = tk.Frame(frame, bg=pegar_cor("rodape"), height=altura_rodape)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

    # Texto ALPHA VERSION
    tamanho_fonte = int(altura_tela * 0.025)
    texto = tk.Label(
        frame,
        text="ALPHA VERSION 1.0",
        bg=pegar_cor("rodape"),
        fg=pegar_cor("texto_rodape"),
        font=("Dubai", tamanho_fonte, "bold"),
        padx=0,
        pady=0
    )
    texto.place(relx=0.09, rely=0.977, anchor="center")

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Kifome")

    # Estado inicial do tema
    janela.tema_escuro = False

    cor_inicial = "#1e272e" if janela.tema_escuro else "#FCB57D"
    janela.configure(bg=cor_inicial)

    # Ícone da Janela
    caminho_icone = resource_path("Imagens/icone.ico")
    if os.path.exists(caminho_icone):
        janela.iconbitmap(caminho_icone)

    # Abre em tela Cheia
    janela.state('zoomed')

    container = tk.Frame(janela, bg=cor_inicial)
    container.pack(fill="both", expand=True)

    def iniciar():
        montar_tela(container, iniciar, janela_principal=janela)

    montar_tela(container, iniciar, janela_principal=janela)
    janela.mainloop()