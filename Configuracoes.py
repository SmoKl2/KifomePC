import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def montar_tela(frame, voltar, janela_principal):
    for widget in frame.winfo_children(): # LIMPA A TELA
        widget.destroy()

    cor_fundo = "#FCB57D"
    frame.config(bg=cor_fundo)

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

#Banco
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

    def voltar_seguro():
        try:
            conn.close()
        except:
            pass
        voltar()

#Código nome kifome
    caminho_imagem = resource_path(r"Imagens\nome kifome.png")
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame, image=img_tk, bg=cor_fundo)
            label_img.pack(pady=10)
        except Exception as e:
            print(f"Erro logo: {e}")

#Código Texto Editar Menu
    def Editar_Menu(event=None):
        for widget in frame.winfo_children():
            widget.destroy()

        import Editar_Menu
        Editar_Menu.montar_tela(
            frame=frame,
            voltar=lambda: montar_tela(frame, voltar, janela_principal),
            janela_principal=janela_principal
        )

    texto_editar = tk.Label(
        frame,
        text="Editar Menu",
        font=("Arial", 18, "bold"),
        fg="#2c3e50",
        bg="#FCB57D",
        cursor="hand2"
    )
    texto_editar.place(relx=0.5, rely=0.5, anchor="center")
    texto_editar.bind("<Button-1>", Editar_Menu)
    texto_editar.bind("<Enter>", lambda e: texto_editar.config(fg="#34495e", font=("Arial", 18, "bold", "underline")))
    texto_editar.bind("<Leave>", lambda e: texto_editar.config(fg="#2c3e50", font=("Arial", 18, "bold")))

#Código botão voltar
    caminho_voltar = resource_path(r"Imagens\voltar.png")
    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)
            janela_principal.lista_imagens.append(img_voltar)

            botao_voltar = tk.Button(
                frame,
                image=img_voltar,
                command=voltar_seguro,
                borderwidth=0,
                highlightthickness=0,
                bg="#FCB57D",
                activebackground="#FCB57D",
                relief="flat",
                cursor="hand2"
            )
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
        except:
            botao_voltar = tk.Button(frame, text="Voltar", font=("Arial", 14),
                                     command=voltar_seguro)
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
    else:
        botao_voltar = tk.Button(frame, text="Voltar", font=("Arial", 14), command=voltar_seguro)
        botao_voltar.place(relx=0.025, rely=0.05, anchor="center")

#Altura janela
    altura_tela = janela_principal.winfo_height()
    if altura_tela <= 1:
        altura_tela = janela_principal.winfo_screenheight()

#Borda branca rodapé
    altura_rodape = int(altura_tela * 0.07)
    rodape = tk.Frame(frame, bg="white", height=altura_rodape)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

#Texto ALPHA VERSION
    tamanho_fonte = int(altura_tela * 0.025)
    texto = tk.Label(
        frame,
        text="ALPHA VERSION 1.0",
        bg="#FEFEFE",
        fg="Black",
        font=("Dubai", tamanho_fonte, "bold"),
        padx=0,
        pady=0
    )
    texto.place(relx=0.09, rely=0.977, anchor="center")