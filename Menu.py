import tkinter as tk
from PIL import Image, ImageTk
import os

def montar_tela(frame, voltar, janela_principal):

    cor_fundo = janela_principal.cget("bg")

    frame.config(bg="#FCB57D")  # Troca pra cor que quiser

    def trocar_bg(cor):
        frame.config(bg=cor)
        label_img.config(bg=cor)
        botao_voltar.config(bg=cor, activebackground=cor)

#Código nome kifome
    caminho_imagem = r"Imagens\nome kifome.png"  # Troca pelo teu caminho

    if os.path.exists(caminho_imagem):
        try:
            # 1. Abre e redimensiona
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))  # Tamanho que quiser

            # 2. Converte pra PhotoImage
            img_tk = ImageTk.PhotoImage(img_original)

            # 3. Cria Label com a imagem
            label_img = tk.Label(frame, image=img_tk, bg="#FCB57D")
            label_img.image = img_tk  # IMPORTANTE: guarda referência pra não sumir
            label_img.pack(pady=15)
            label_img.place(relx=0.5, rely=0.16, anchor="center")

        except Exception as e:
            tk.Label(frame, text=f"Erro ao carregar imagem: {e}", fg="red", bg="#FCB57D").pack()
    else:
        tk.Label(frame, text="Imagem não encontrada", fg="red", bg="#FCB57D").pack()

    #Código botão voltar

    caminho_voltar = r"Imagens\voltar.png"  # Troca pelo caminho da tua imagem de voltar

    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))  # Ajusta o tamanho
            img_voltar = ImageTk.PhotoImage(img_voltar_original)

            botao_voltar = tk.Button(
                frame,
                image=img_voltar,
                command=voltar,  # Usa o callback que veio do main
                borderwidth=0,
                highlightthickness=0,
                bg="#FCB57D",
                activebackground="#FCB57D",
                relief="flat",
                cursor="hand2"
            )
            botao_voltar.image = img_voltar  # Guarda referência
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")

        except Exception as e:
            #Erro
            tk.Button(frame, text="Voltar pro Menu", font=("Arial", 14), command=voltar).place(relx=0.5, rely=0.9,
                                                                                               anchor="center")
    else:
        # Se não achar a imagem, usa botão normal
        tk.Button(frame, text="Voltar pro Menu", font=("Arial", 14), command=voltar).place(relx=0.5, rely=0.9,
                                                                                           anchor="center")