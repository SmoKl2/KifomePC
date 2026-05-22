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


#Código Texto Editar Menu

    def Editar_Menu(event=None):
        for widget in frame.winfo_children():
            widget.destroy()

        frame.tkraise()

        caminho = r"Editar_Menu.py"

        try:
            if "Editar_Menu" in sys.modules:
                del sys.modules["Editar_Menu"]

            spec = importlib.util.spec_from_file_location("Editar_Menu", caminho)
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

    texto_editar = tk.Label(
        frame,
        text="Editar Menu",  # mudei o texto
        font=("Arial", 18, "bold"),
        fg="#2c3e50",
        bg="#FCB57D",
        cursor="hand2"
    )
    texto_editar.place(relx=0.5, rely=0.5, anchor="center")
    texto_editar.bind("<Button-1>", Editar_Menu)

    texto_editar.bind("<Enter>", lambda e: texto_editar.config(fg="#34495e", font=("Arial", 18, "bold", "underline")))
    texto_editar.bind("<Leave>", lambda e: texto_editar.config(fg="#2c3e50", font=("Arial", 18, "bold")))

#Código nome kifome
    caminho_imagem = r"Imagens\nome kifome.png"

    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))

            img_tk = ImageTk.PhotoImage(img_original)
            label_img = tk.Label(frame, image=img_tk, bg="#FCB57D")
            label_img.image = img_tk
            label_img.place(relx=0.5, rely=0.16, anchor="center")

        except Exception as e:
            label_img = tk.Label(frame, text=f"Erro ao carregar imagem: {e}", fg="red", bg="#FCB57D")
            label_img.place(relx=0.5, rely=0.16, anchor="center")
    else:
        label_img = tk.Label(frame, text="Imagem não encontrada", fg="red", bg="#FCB57D")
        label_img.place(relx=0.5, rely=0.16, anchor="center")

#Código botão voltar

    caminho_voltar = r"Imagens\voltar.png"

    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)

            botao_voltar = tk.Button(
                frame,
                image=img_voltar,
                command=voltar,
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
            botao_voltar = tk.Button(frame, text="Voltar pro Menu", font=("Arial", 14), command=voltar)
            botao_voltar.place(relx=0.5, rely=0.9, anchor="center")
    else:
        botao_voltar = tk.Button(frame, text="Voltar pro Menu", font=("Arial", 14), command=voltar)
        botao_voltar.place(relx=0.5, rely=0.9, anchor="center")

