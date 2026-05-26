import tkinter as tk
from PIL import Image, ImageTk
import importlib.util
import sys
import os
import sqlite3

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pasta temporária do PyInstaller
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def montar_tela(frame, voltar, janela_principal):
    for widget in frame.winfo_children():
        widget.destroy()

    cor_fundo = "#FCB57D"

    frame.config(bg="#FCB57D")

#Guardar lista de imagens caso não exista
    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

    conn = sqlite3.connect(resource_path("cardapio.db"))  # MUDOU AQUI
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            preco REAL,
            descricao TEXT,
            imagem TEXT
        )
    """)
    conn.commit()


#Código nome kifome
    caminho_imagem = resource_path(r"Imagens\nome kifome.png")  # MUDOU AQUI
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame, image=img_tk, bg=cor_fundo)

            label_img.pack(pady=10)

        except:
            pass

#Código botão Menu
    def abrir_menu():
        for widget in frame.winfo_children():
            widget.destroy()

        caminho = resource_path("Menu.py")
        try:
            if "Menu" in sys.modules:
                del sys.modules["Menu"]

            spec = importlib.util.spec_from_file_location("Menu", caminho)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            modulo.montar_tela(frame, voltar, janela_principal)

        except Exception as e:
            tk.Label(frame, text=f"Erro: {e}", fg="red", bg="#FCB57D").pack()

    imagem_original = Image.open(resource_path(r"Imagens\Menu.png"))
    imagem_original = imagem_original.resize((585, 500))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_menu,
        borderwidth=0,
        highlightthickness=0,
        bg="#FCB57D",
        activebackground="#FCB57D",
        relief="flat",
        cursor="hand2",
    )
    botao.place(relx=0.17, rely=0.6, anchor="center")

#Código botão Carrinho
    def abrir_carrinho():
        for widget in frame.winfo_children():
            widget.destroy()

        caminho = r"Carrinho.py"
        try:
            if "Carrinho" in sys.modules:
                del sys.modules["Carrinho"]

            spec = importlib.util.spec_from_file_location("Carrinho", caminho)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            modulo.montar_tela(
                frame=frame,
                voltar=lambda: montar_tela(frame, voltar, janela_principal),
                janela_principal=janela_principal
            )
        except Exception as e:
            tk.Label(frame, text=f"Erro: {e}", fg="red", bg="#FCB57D").pack()

    imagem_original = Image.open(resource_path(r"Imagens\Carrinho.png"))
    imagem_original = imagem_original.resize((585, 500))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_carrinho,
        borderwidth=0,
        highlightthickness=0,
        bg="#FCB57D",
        activebackground="#FCB57D",
        relief="flat",
        cursor="hand2",
    )
    botao.place(relx=0.497, rely=0.6, anchor="center")

#Código botão Configurações
    def abrir_config():
        for widget in frame.winfo_children():
            widget.destroy()

        caminho = r"Configuracoes.py"
        try:
            if "Configuracoes" in sys.modules:
                del sys.modules["Configuracoes"]

            spec = importlib.util.spec_from_file_location("Configuracoes", caminho)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            modulo.montar_tela(
                frame=frame,
                voltar=lambda: montar_tela(frame, voltar, janela_principal),
                janela_principal=janela_principal
            )
        except Exception as e:
            tk.Label(frame, text=f"Erro: {e}", fg="red", bg="#FCB57D").pack()

    imagem_original = Image.open(resource_path(r"Imagens\Configurações.png"))
    imagem_original = imagem_original.resize((585, 500))
    imagem_botao = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_botao)

    botao = tk.Button(
        frame,
        image=imagem_botao,
        command=abrir_config,
        borderwidth=0,
        highlightthickness=0,
        bg="#FCB57D",
        activebackground="#FCB57D",
        relief="flat",
        cursor="hand2",
    )
    botao.place(relx=0.825, rely=0.6, anchor="center")

#Borda branca rodapé
    rodape = tk.Frame(frame, bg="white", height=55)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

    def ao_sair():
        conn.close()
        voltar()

    #Texto ALPHA VERSION
    texto = tk.Label(
        frame,
        text="ALPHA VERSION 1.0",
        bg="#FEFEFE",
        fg="Black",
        font=("Dubai", 20, "bold"),
        padx=0,
        pady=0
    )
    texto.place(relx=0.07, rely=0.977, anchor="center")


#Configurações janela

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Kifome")
    janela.geometry("1280x720")
    janela.configure(bg="#FCB57D")
    janela.iconbitmap(resource_path(r"Imagens\Logo.ico"))

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    janela.geometry(f"{largura_tela}x{altura_tela}+0+0")
    janela.state('zoomed')

    container = tk.Frame(janela, bg="#FCB57D")
    container.pack(fill="both", expand=True)

    montar_tela(container, voltar=lambda: None, janela_principal=janela)

    janela.mainloop()