import tkinter as tk
from PIL import Image, ImageTk
import os

def montar_tela(frame, voltar, janela_principal):

    cor_fundo = janela_principal.cget("bg")

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
            label_img = tk.Label(frame, image=img_tk, bg="#2d2d2d")
            label_img.image = img_tk  # IMPORTANTE: guarda referência pra não sumir
            label_img.pack(pady=15)
            label_img.place(relx=0.5, rely=0.16, anchor="center")

        except Exception as e:
            tk.Label(frame, text=f"Erro ao carregar imagem: {e}", fg="red", bg="#2d2d2d").pack()
    else:
        tk.Label(frame, text="Imagem não encontrada", fg="red", bg="#2d2d2d").pack()

    tk.Button(
        frame,
        text="Voltar pro Menu",
        font=("Arial", 14),
        command=voltar
    ).pack(pady=20)