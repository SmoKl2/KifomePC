import tkinter as tk
from PIL import Image, ImageTk
import os

def montar_tela(frame, voltar, janela_principal):

    cor_fundo = janela_principal.cget("bg")

#Trocar pra cor background

    frame.config(bg="#FCB57D")

    def trocar_bg(cor):
        frame.config(bg=cor)
        label_img.config(bg=cor)
        if 'botao_voltar' in locals():
            botao_voltar.config(bg=cor, activebackground=cor)
        if 'botao_continuar' in locals():
            botao_continuar.config(bg=cor, activebackground=cor)

# Tamanho da janela principal

            janela_principal.update_idletasks()  # Garante que pegou o tamanho certo
            largura_janela = janela_principal.winfo_width()
            altura_janela = janela_principal.winfo_height()

# Correção erro janela não renderizando

            if largura_janela <= 1:
                largura_janela = janela_principal.winfo_screenwidth()
                altura_janela = janela_principal.winfo_screenheight()

# Escala baseado em 1920x1080

            escala_w = largura_janela / 1920
            escala_h = altura_janela / 1080
            escala = min(escala_w, escala_h)

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

#Código botão continuar
    caminho_continuar = r"Imagens\continuar.png"

    if os.path.exists(caminho_continuar):
        try:
            img_continuar_original = Image.open(caminho_continuar).convert("RGBA")
            img_continuar_original = img_continuar_original.resize((60, 60))
            img_continuar = ImageTk.PhotoImage(img_continuar_original)

            botao_continuar = tk.Button(
                frame,
                image=img_continuar,
                command=lambda: print("Continuar clicado"),  # Troca pela tua função
                borderwidth=0,
                highlightthickness=0,
                bg="#FCB57D",
                activebackground="#FCB57D",
                relief="flat",
                cursor="hand2"
            )
            botao_continuar.image = img_continuar
            botao_continuar.place(relx=0.975, rely=0.6, anchor="center")

        except Exception as e:
            botao_continuar = tk.Button(frame, text="Continuar", font=("Arial", 14), command=lambda: print("Continuar clicado"))
            botao_continuar.place(relx=0.975, rely=0.95, anchor="center")
    else:
        botao_continuar = tk.Button(frame, text="Continuar", font=("Arial", 14), command=lambda: print("Continuar clicado"))
        botao_continuar.place(relx=0.975, rely=0.95, anchor="center")

#Borda branca rodapé
    rodape = tk.Frame(frame, bg="white", height=55)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

#Texto ALPHA VERSION
    texto = tk.Label(
        frame,
        text="ALPHA VERSION 1.0",
        bg="white",
        fg="Black",
        font=("Dubai", 20, "bold"),
        padx=0,
        pady=0
    )
    texto.place(relx=0.07, rely=0.977, anchor="center")