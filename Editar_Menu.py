import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import importlib.util

def montar_tela(frame, voltar, janela_principal):

    cor_fundo = janela_principal.cget("bg")

#Trocar pra cor background

    frame.config(bg="#FCB57D")

    def trocar_bg(cor):
        frame.config(bg=cor)
        label_img.config(bg=cor)
        botao_voltar.config(bg=cor, activebackground=cor)

#Tamanho da janela principal

        janela_principal.update_idletasks()  # Garante que pegou o tamanho certo
        largura_janela = janela_principal.winfo_width()
        altura_janela = janela_principal.winfo_height()

#Correção erro janela não renderizando

        if largura_janela <= 1:
            largura_janela = janela_principal.winfo_screenwidth()
            altura_janela = janela_principal.winfo_screenheight()

#Escala baseado em 1920x1080

        escala_w = largura_janela / 1920
        escala_h = altura_janela / 1080
        escala = min(escala_w, escala_h)

#Código nome kifome

    caminho_imagem = r"Imagens\nome kifome.png"

    if os.path.exists(caminho_imagem):
        try:

            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))  # Tamanho que quiser

            img_tk = ImageTk.PhotoImage(img_original)

            label_img = tk.Label(frame, image=img_tk, bg="#FCB57D")
            label_img.image = img_tk  # IMPORTANTE: guarda referência pra não sumir
            label_img.pack(pady=15)
            label_img.place(relx=0.5, rely=0.16, anchor="center")

        except Exception as e:
            tk.Label(frame, text=f"Erro ao carregar imagem: {e}", fg="red", bg="#FCB57D").pack()
    else:
        tk.Label(frame, text="Imagem não encontrada", fg="red", bg="#FCB57D").pack()

#Código botão voltar

    def Configuracoes():
        for widget in frame.winfo_children():
            widget.destroy()

        frame.tkraise()

        caminho = r"Configuracoes.py"

        try:
            if "Configuracoes" in sys.modules:
                del sys.modules["Configuracoes"]

            spec = importlib.util.spec_from_file_location("Configuracoes", caminho)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            # Passa: frame, função de voltar e a janela principal
            modulo.montar_tela(
                frame=frame,
                voltar=lambda: frame.tkraise(),
                janela_principal=janela_principal
            )

        except Exception as e:
            tk.Label(frame, text=f"Erro: {e}", fg="red", bg="#FCB57D").pack()

    caminho_voltar = r"Imagens\voltar.png"

    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)

            botao_voltar = tk.Button(
                frame,
                image=img_voltar,
                command=Configuracoes,  # chama a função nova
                borderwidth=0,
                highlightthickness=0,
                bg="#FCB57D",
                activebackground="#FCB57D",
                relief="flat",
                cursor="hand2"
            )
            botao_voltar.image = img_voltar
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")

        except Exception as e:
            botao_voltar = tk.Button(frame, text="Voltar pra Configuracoes", font=("Arial", 14), command=Configuracoes)
            botao_voltar.place(relx=0.5, rely=0.9, anchor="center")
    else:
        botao_voltar = tk.Button(frame, text="Voltar pra Configuracoes", font=("Arial", 14), command=Configuracoes)
        botao_voltar.place(relx=0.5, rely=0.9, anchor="center")