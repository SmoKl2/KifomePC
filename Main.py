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

#Código adicionar botões e suas imagens
script_dir = os.path.dirname(__file__)
img1_path = os.path.join(script_dir, "assets", r"D:\Programacao\KifomePC\Imagens\Menu.png")
img2_path = os.path.join(script_dir, "assets", r"D:\Programacao\KifomePC\Imagens\Carrinho.png")
img3_path = os.path.join(script_dir, "assets", r"D:\Programacao\KifomePC\Imagens\Configurações.png")

# Carregar e redimensionar a imagem
img1 = ctk.CTkImage(light_image=Image.open(img1_path), size=(585, 500))
img2 = ctk.CTkImage(light_image=Image.open(img2_path), size=(585, 500))
img3 = ctk.CTkImage(light_image=Image.open(img3_path), size=(585, 500))

#Funções dos botões
def acao_1():
    print("Botão 1 pressionado")

def acao_2():
    print("Botão 2 pressionado")

def acao_3():
    print("Botão 3 pressionado")

#Criar botões
# fg_color="transparent" remove a cor de fundo do botão
# text="" remove o texto padrão
btn1 = ctk.CTkButton(app, image=img1, text="", fg_color="transparent",
                     hover_color="#555555", width=50, height=50, command=acao_1)
btn1.pack(pady=20)
btn1.place(relx=0.17, rely=0.6, anchor="center")

btn2 = ctk.CTkButton(app, image=img2, text="", fg_color="transparent",
                     hover_color="#555555", width=50, height=50, command=acao_2)
btn2.pack(pady=20)
btn2.place(relx=0.497, rely=0.6, anchor="center")

btn3 = ctk.CTkButton(app, image=img3, text="", fg_color="transparent",
                     hover_color="#555555", width=50, height=50, command=acao_3)
btn3.pack(pady=20)
btn3.place(relx=0.825, rely=0.6, anchor="center")

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
label_imagem.place(relx=0.5, rely=0.16, anchor="center")  # posição na tela

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