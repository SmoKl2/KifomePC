import tkinter as tk
from PIL import Image, ImageTk
import importlib.util
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pasta temporária do PyInstaller
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def montar_tela(frame, voltar, janela_principal):
    for widget in frame.winfo_children():
        widget.destroy()

    frame.config(bg="#FCB57D")

#Guardar lista de imagens caso não exista
    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

#Código nome kifome
    imagem_original = Image.open(r"Imagens\nome kifome.png").convert("RGBA")
    imagem_original = imagem_original.resize((600, 220))
    imagem_menu = ImageTk.PhotoImage(imagem_original)
    janela_principal.lista_imagens.append(imagem_menu)

    label_imagem = tk.Label(
        frame,
        image=imagem_menu,
        bg="#FCB57D",
    )
    label_imagem.place(relx=0.5, rely=0.16, anchor="center")

#Código botão Menu
    def abrir_menu():
        for widget in frame.winfo_children():
            widget.destroy()

        caminho = r"Menu.py"
        try:
            if "Menu" in sys.modules:
                del sys.modules["Menu"]

            spec = importlib.util.spec_from_file_location("Menu", caminho)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            modulo.montar_tela(
                frame=frame,
                voltar=lambda: montar_tela(frame, voltar, janela_principal),
                janela_principal=janela_principal
            )
        except Exception as e:
            tk.Label(frame, text=f"Erro: {e}", fg="red", bg="#FCB57D").pack()

    imagem_original = Image.open(r"Imagens\Menu.png").convert("RGBA")
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

    imagem_original = Image.open(r"Imagens\Carrinho.png").convert("RGBA")
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

    imagem_original = Image.open(r"Imagens\Configurações.png").convert("RGBA")
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