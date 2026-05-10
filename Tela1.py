import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

#Código Janela

janela = tk.Tk()
janela.title("Tela1")
janela.geometry("1280x720")
janela.configure(bg="#FCB57D")

#Código Imagem Menu

imagem_original = Image.open(r"D:\Programacao\KifomePC\Imagens\Menu.png")
imagem_original = imagem_original.resize((485, 385))
imagem_botao = ImageTk.PhotoImage(imagem_original)

def clicar():
    print("Botão clicado!")

botao = tk.Button(
janela, image=imagem_botao, command=clicar, bd=0, cursor="hand2"

)
botao.pack(pady=50)
botao.place(x=100, y=150)
botao.image = imagem_botao

# Código Imagem Carrinho

imagem_original = Image.open(r"D:\Programacao\KifomePC\Imagens\Carrinho.png")
imagem_original = imagem_original.resize((485, 385))
imagem_botao = ImageTk.PhotoImage(imagem_original)


def clicar():
    print("Botão clicado!")

botao = tk.Button(
    janela, image=imagem_botao, command=clicar, bd=0, cursor="hand2"

)
botao.pack(pady=50)
botao.place(x=600, y=150)
botao.image = imagem_botao

# Código Imagem Configurações

imagem_original = Image.open(r"D:\Programacao\KifomePC\Imagens\Configurações.png")
imagem_original = imagem_original.resize((485, 385))
imagem_botao = ImageTk.PhotoImage(imagem_original)


def clicar():
    print("Botão clicado!")

botao = tk.Button(
    janela, image=imagem_botao, command=clicar, bd=0, cursor="hand2"

)
botao.pack(pady=50)
botao.place(x=1100, y=150)
botao.image = imagem_botao


janela.mainloop()