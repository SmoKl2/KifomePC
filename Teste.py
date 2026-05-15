import tkinter as tk
from PIL import Image, ImageTk

janela = tk.Tk()
janela.title("Menu")
janela.geometry("800x600")

# Container que vai segurar todas as telas no mesmo lugar
container = tk.Frame(janela)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# --- TELA 1: MENU COM BOTÃO ---
tela_menu = tk.Frame(container, bg=janela.cget("bg"))
tela_menu.grid(row=0, column=0, sticky="nsew")

imagem_original = Image.open(r"D:\Programacao\KifomePC\Imagens\Menu.png").convert("RGBA")
imagem_original = imagem_original.resize((585, 500))
imagem_botao = ImageTk.PhotoImage(imagem_original)

def abrir_tela_nova():
    tela_nova.tkraise()  # Joga a tela nova pra frente

botao = tk.Button(
    tela_menu,
    image=imagem_botao,
    command=abrir_tela_nova,  # Agora chama a função que troca de tela
    borderwidth=0,
    highlightthickness=0,
    bg=janela.cget("bg"),
    activebackground=janela.cget("bg"),
    relief="flat",
    cursor="hand2",
)
botao.image = imagem_botao  # Evita garbage collection
botao.place(relx=0.17, rely=0.6, anchor="center")

# --- TELA 2: A "TELA NOVA" QUE O BOTÃO ABRE ---
tela_nova = tk.Frame(container, bg="#2d2d2d")
tela_nova.grid(row=0, column=0, sticky="nsew")

tk.Label(tela_nova, text="Tela Nova Aberta", font=("Arial", 24), bg="#2d2d2d", fg="white").pack(pady=50)

# Botão pra voltar pro menu
tk.Button(
    tela_nova,
    text="Voltar pro Menu",
    font=("Arial", 14),
    command=lambda: tela_menu.tkraise()
).pack(pady=20)

# Começa mostrando o menu
tela_menu.tkraise()

janela.mainloop()