import tkinter as tk
from PIL import Image, ImageTk
import importlib.util
import sys

# Código Janela

janela = tk.Tk()
janela.title("Main")
janela.geometry("1280x720")
janela.configure(bg="#FCB57D")
janela.title("Kifome")
janela.iconbitmap(r"Imagens\Logo.ico")

#Adaptar Resolução
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
janela.geometry(f"{largura_tela}x{altura_tela}+0+0")
janela.state('zoomed')  # Maximiza no Windows
janela.configure(bg="#FCB57D")

#Escala proporcional baseada na resolução
escala_w = largura_tela / 1920  # Base 1920px
escala_h = altura_tela / 1080   # Base 1080px
escala = min(escala_w, escala_h)  # Mantém proporção

# Container que vai segurar todas as telas
container = tk.Frame(janela, bg="#FCB57D")
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

tela_menu = tk.Frame(container, bg=janela.cget("bg"))
tela_menu.grid(row=0, column=0, sticky="nsew")

tela_nova = tk.Frame(container, bg="#2d2d2d")
tela_nova.grid(row=0, column=0, sticky="nsew")

#Código nome kifome
imagem_original = Image.open(r"Imagens\nome kifome.png").convert("RGBA")
imagem_original = imagem_original.resize((600, 220))
imagem_menu = ImageTk.PhotoImage(imagem_original)

label_imagem = tk.Label(
    tela_menu,
    image=imagem_menu,
    bg=janela.cget("bg"),
)
label_imagem.image = imagem_menu  # Guarda referência
label_imagem.place(relx=0.5, rely=0.16, anchor="center")

#Código botão Menu

def abrir_tela_nova():
    for widget in tela_nova.winfo_children():
        widget.destroy()

    tela_nova.tkraise()

    caminho = r"Menu.py"

    try:
        if "Menu" in sys.modules:
            del sys.modules["Menu"]

        spec = importlib.util.spec_from_file_location("Menu", caminho)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        # Passa: frame, função de voltar, e a janela principal se precisar
        modulo.montar_tela(
            frame=tela_nova,
            voltar=lambda: tela_menu.tkraise(),
            janela_principal=janela  # Se precisar usar janela.cget() etc
        )

    except Exception as e:
        tk.Label(tela_nova, text=f"Erro: {e}", fg="red", bg="#2d2d2d").pack()

imagem_original = Image.open(r"Imagens\Menu.png").convert("RGBA")
imagem_original = imagem_original.resize((585, 500))
imagem_botao = ImageTk.PhotoImage(imagem_original)

botao = tk.Button(
    tela_menu,
    image=imagem_botao,
    command=abrir_tela_nova,
    borderwidth=0,
    highlightthickness=0,
    bg=janela.cget("bg"),
    activebackground=janela.cget("bg"),
    relief="flat",
    cursor="hand2",
)
botao.image = imagem_botao
botao.place(relx=0.17, rely=0.6, anchor="center")

tela_menu.tkraise()

#Código botão Carrinho

def abrir_tela_nova():
    for widget in tela_nova.winfo_children():
        widget.destroy()

    tela_nova.tkraise()

    caminho = r"Menu.py"

    try:
        if "Menu" in sys.modules:
            del sys.modules["Menu"]

        spec = importlib.util.spec_from_file_location("Menu", caminho)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        # Passa: frame, função de voltar, e a janela principal se precisar
        modulo.montar_tela(
            frame=tela_nova,
            voltar=lambda: tela_menu.tkraise(),
            janela_principal=janela  # Se precisar usar janela.cget() etc
        )

    except Exception as e:
        tk.Label(tela_nova, text=f"Erro: {e}", fg="red", bg="#2d2d2d").pack()

imagem_original = Image.open(r"Imagens\Carrinho.png").convert("RGBA")
imagem_original = imagem_original.resize((585, 500))
imagem_botao = ImageTk.PhotoImage(imagem_original)

botao = tk.Button(
    tela_menu,
    image=imagem_botao,
    command=abrir_tela_nova,
    borderwidth=0,
    highlightthickness=0,
    bg=janela.cget("bg"),
    activebackground=janela.cget("bg"),
    relief="flat",
    cursor="hand2",
)
botao.image = imagem_botao
botao.place(relx=0.497, rely=0.6, anchor="center")

tela_menu.tkraise()

#Código botão Configurações

def abrir_tela_nova():
    for widget in tela_nova.winfo_children():
        widget.destroy()

    tela_nova.tkraise()

    caminho = r"Menu.py"

    try:
        if "Menu" in sys.modules:
            del sys.modules["Menu"]

        spec = importlib.util.spec_from_file_location("Menu", caminho)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        # Passa: frame, função de voltar, e a janela principal se precisar
        modulo.montar_tela(
            frame=tela_nova,
            voltar=lambda: tela_menu.tkraise(),
            janela_principal=janela  # Se precisar usar janela.cget() etc
        )

    except Exception as e:
        tk.Label(tela_nova, text=f"Erro: {e}", fg="red", bg="#2d2d2d").pack()

imagem_original = Image.open(r"Imagens\Configurações.png").convert("RGBA")
imagem_original = imagem_original.resize((585, 500))
imagem_botao = ImageTk.PhotoImage(imagem_original)

botao = tk.Button(
    tela_menu,
    image=imagem_botao,
    command=abrir_tela_nova,
    borderwidth=0,
    highlightthickness=0,
    bg=janela.cget("bg"),
    activebackground=janela.cget("bg"),
    relief="flat",
    cursor="hand2",
)
botao.image = imagem_botao
botao.place(relx=0.825, rely=0.6, anchor="center")

tela_menu.tkraise()

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