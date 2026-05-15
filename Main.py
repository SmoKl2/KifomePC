import tkinter as tk
from PIL import Image, ImageTk
import os

# Código Janela

janela = tk.Tk()
janela.title("Tela1")
janela.geometry("1280x720")
janela.configure(bg="#FCB57D")
janela.title("Kifome")
janela.iconbitmap(r"D:\Programacao\KifomePC\Imagens\Logo.ico")

#Código nome kifome

img = Image.open(r"D:\Programacao\KifomePC\Imagens\nome kifome.png")
img_redimensionada = img.resize((600, 220))  # largura, altura
img_tk = ImageTk.PhotoImage(img_redimensionada)

label = tk.Label(
    janela,
    image=img_tk,
    bg=janela.cget("bg")
)
label.image = img_tk
label.place(relx=0.5, rely=0.16, anchor="center")

#Código botão Menu

imagem_original = Image.open(r"D:\Programacao\KifomePC\Imagens\Menu.png").convert("RGBA")
imagem_original = imagem_original.resize((585, 500))
imagem_botao = ImageTk.PhotoImage(imagem_original)

def clicar():
    print("Botão clicado!")

botao = tk.Button(
    janela,
    image=imagem_botao,
    command=clicar,
    borderwidth=0,           # tira borda
    highlightthickness=0,    # tira contorno de foco
    bg=janela.cget("bg"),    # fundo igual da janela
    activebackground=janela.cget("bg"),  # não pisca quando clica
    relief="flat",           # tira efeito 3D
    cursor="hand2",
)

botao.image = imagem_botao
botao.place(relx=0.17, rely=0.6, anchor="center")  # responsivo

#Código botão Carrinho

imagem_original = Image.open(r"D:\Programacao\KifomePC\Imagens\Carrinho.png").convert("RGBA")
imagem_original = imagem_original.resize((585, 500))
imagem_botao = ImageTk.PhotoImage(imagem_original)

def clicar():
    print("Botão clicado!")

botao = tk.Button(
    janela,
    image=imagem_botao,
    command=clicar,
    borderwidth=0,           # tira borda
    highlightthickness=0,    # tira contorno de foco
    bg=janela.cget("bg"),    # fundo igual da janela
    activebackground=janela.cget("bg"),  # não pisca quando clica
    relief="flat",           # tira efeito 3D
    cursor="hand2"
)
botao.image = imagem_botao
botao.place(relx=0.497, rely=0.6, anchor="center")  # responsivo

#Código botão Configurações

imagem_original = Image.open(r"D:\Programacao\KifomePC\Imagens\Configurações.png").convert("RGBA")
imagem_original = imagem_original.resize((585, 500))
imagem_botao = ImageTk.PhotoImage(imagem_original)

def clicar():
    print("Botão clicado!")

botao = tk.Button(
    janela,
    image=imagem_botao,
    command=clicar,
    borderwidth=0,           # tira borda
    highlightthickness=0,    # tira contorno de foco
    bg=janela.cget("bg"),    # fundo igual da janela
    activebackground=janela.cget("bg"),  # não pisca quando clica
    relief="flat",           # tira efeito 3D
    cursor="hand2"
)
botao.image = imagem_botao
botao.place(relx=0.825, rely=0.6, anchor="center")  # responsivo

# BORDA BRANCA NO RODAPÉ
rodape = tk.Frame(janela, bg="white", height=55)
rodape.pack(side="bottom", fill="x")  # fill="x" = estica na horizontal toda

#Texto ALPHA VERSION

texto = tk.Label(
    janela,
    text="ALPHA VERSION 1.0",
    bg="#FEFEFE",
    fg="Black",
    font=("Dubai", 30, "bold"),
    padx=0,
    pady=0
)
texto.place(relx=0.1, rely=0.98, anchor="center")

janela.mainloop()