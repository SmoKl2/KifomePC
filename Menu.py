import customtkinter as ctk
from PIL import Image
import os

# Código Janela

ctk.set_appearance_mode("Dark")  # Modo escuro
app = ctk.CTk()
app.geometry("1280x720")
app.title("Botões Transparentes")
app.configure(fg_color="#FCB57D")
app.title("Kifome")
app.iconbitmap(r"D:\Programacao\KifomePC\Imagens\Logo.ico")

#Imagem Nome Kifome

imagem = ctk.CTkImage(
    light_image=Image.open(r"D:\Programacao\KifomePC\Imagens\nome kifome.png"),  # modo claro
    dark_image=Image.open(r"D:\Programacao\KifomePC\Imagens\nome kifome.png"),   # modo escuro, pode ser a mesma
    size=(600, 220)  # tamanho que vai aparecer na tela
)

label_imagem = ctk.CTkLabel(
    app,
    image=imagem,
    text=""  # vazio pra não aparecer texto junto
)
label_imagem.place(relx=0.55, rely=0.16, anchor="center")  # posição na tela

# Frame = borda branca rodapé
borda_branca = ctk.CTkFrame(
    app,
    height=40,           # espessura da borda
    fg_color="white",   # cor branca
    corner_radius=0     # sem canto arredondado
)
borda_branca.place(relx=0, rely=1.0, relwidth=1.0, anchor="sw")

# Texto ALPHA VERSION 1.0
nome = ctk.CTkLabel(
    app,
    text="ALPHA VERSION 1.0",
    font=("Dubai", 20, "bold"),
    text_color="black",
    fg_color="white"
)
nome.place(relx=0.05, rely=1.008, y=-10, anchor="s")  # y=-10 sobe 10px do fundo


app.mainloop()