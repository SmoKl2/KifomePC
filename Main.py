import tkinter as tk
from PIL import Image, ImageTk
import Menu
import Carrinho
import Configuracoes
import sys
import os
import sqlite3

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def montar_tela(frame, voltar, janela_principal):
    for widget in frame.winfo_children():
        widget.destroy()

    cor_fundo = "#FCB57D"
    frame.config(bg="#FCB57D")

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

    # --- DEFINE VOLTAR_PRO_MENU AQUI, ANTES DE USAR ---
    def voltar_pro_menu():
        montar_tela(frame, voltar_pro_menu, janela_principal)

    conn = sqlite3.connect(resource_path("cardapio.db"))
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

    # Código nome kifome
    caminho_imagem = resource_path(r"Imagens\nome kifome.png")
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame, image=img_tk, bg=cor_fundo)
            label_img.pack(pady=10)
        except:
            pass

    #Código botão Menu
    def abrir_menu():
        for widget in frame.winfo_children():
            widget.destroy()
        Menu.montar_tela(frame, voltar_pro_menu, janela_principal)

    imagem_original = Image.open(resource_path(r"Imagens\Menu.png"))
    imagem_original = imagem_original.resize((585, 500))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_menu,
        borderwidth=0,
        highlightthickness=0,
        bg="#FCB57D",
        activebackground="#FCB57D",
        relief="flat",
        cursor="hand2",
    )
    botao.place(relx=0.17, rely=0.6, anchor="center")

    #Código botão Carrinho
    def abrir_carrinho():
        for widget in frame.winfo_children():
            widget.destroy()
        Carrinho.montar_tela(frame, voltar_pro_menu, janela_principal) # AGORA EXISTE

    imagem_original = Image.open(resource_path(r"Imagens\Carrinho.png"))
    imagem_original = imagem_original.resize((585, 500))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_carrinho,
        borderwidth=0,
        highlightthickness=0,
        bg="#FCB57D",
        activebackground="#FCB57D",
        relief="flat",
        cursor="hand2",
    )
    botao.place(relx=0.497, rely=0.6, anchor="center")

    #Código botão Configurações
    def abrir_config():
        for widget in frame.winfo_children():
            widget.destroy()
        Configuracoes.montar_tela(frame, voltar_pro_menu, janela_principal)

    imagem_original = Image.open(resource_path(r"Imagens\Configurações.png"))
    imagem_original = imagem_original.resize((585, 500))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_config,
        borderwidth=0,
        highlightthickness=0,
        bg="#FCB57D",
        activebackground="#FCB57D",
        relief="flat",
        cursor="hand2",
    )
    botao.place(relx=0.825, rely=0.6, anchor="center")

    #Borda branca rodapé
    rodape = tk.Frame(frame, bg="white", height=55)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

    #Texto ALPHA VERSION
    texto = tk.Label(
        frame,
        text="ALPHA VERSION 1.0",
        bg="#FEFEFE",
        fg="Black",
        font=("Dubai", 20, "bold"),
        padx=0,
        pady=0
    )
    texto.place(relx=0.07, rely=0.977, anchor="center")

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Kifome")
    janela.geometry("1280x720")
    janela.configure(bg="#FCB57D")
    janela.iconbitmap(resource_path(r"Imagens\Logo.ico"))

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    janela.geometry(f"{largura_tela}x{altura_tela}+0+0")
    janela.state('zoomed')

    container = tk.Frame(janela, bg="#FCB57D")
    container.pack(fill="both", expand=True)

    # AQUI TAMBÉM PRECISA DA FUNÇÃO
    def iniciar():
        montar_tela(container, iniciar, janela_principal=janela)

    montar_tela(container, iniciar, janela_principal=janela)

    janela.mainloop()