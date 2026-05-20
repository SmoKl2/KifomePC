import tkinter as tk
from PIL import Image, ImageTk
import importlib.util
import sys
import os

janela = tk.Tk()
janela.title("Menu")
janela.geometry("800x600")

container = tk.Frame(janela, bg="#1e1e1e")
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

tela_menu = tk.Frame(container, bg=janela.cget("bg"))
tela_menu.grid(row=0, column=0, sticky="nsew")

tela_nova = tk.Frame(container, bg="#2d2d2d")
tela_nova.grid(row=0, column=0, sticky="nsew")


def abrir_tela_nova():
    for widget in tela_nova.winfo_children():
        widget.destroy()

    tela_nova.tkraise()

    caminho = r"D:\Programacao\KifomePC\Menu.py"

    try:
        if "tela_secundaria" in sys.modules:
            del sys.modules["tela_secundaria"]

        spec = importlib.util.spec_from_file_location("tela_secundaria", caminho)
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


imagem_original = Image.open(r"D:\Programacao\KifomePC\Imagens\Menu.png").convert("RGBA")
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
janela.mainloop()