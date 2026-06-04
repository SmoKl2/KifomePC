import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def montar_tela(frame, voltar, janela_principal):
    for widget in frame.winfo_children():
        widget.destroy()

    # --- SISTEMA DE TEMAS ---
    if not hasattr(janela_principal, 'tema_escuro'):
        janela_principal.tema_escuro = False

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

    temas = {
        "claro": {
            "fundo": "#FCB57D",
            "texto": "#2c3e50",
            "texto_hover": "#34495e",
            "rodape": "white",
            "texto_rodape": "Black"
        },
        "escuro": {
            "fundo": "#2c3e50",
            "texto": "#ecf0f1",
            "texto_hover": "#bdc3c7",
            "rodape": "#1a252f",
            "texto_rodape": "#ecf0f1"
        }
    }

    def pegar_cor(chave):
        tema_atual = "escuro" if janela_principal.tema_escuro else "claro"
        return temas[tema_atual][chave]

    frame.config(bg=pegar_cor("fundo"))

    # Banco
    conn = sqlite3.connect(resource_path("cardapio.db"))
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

    def voltar_seguro():
        try:
            conn.close()
        except:
            pass
        voltar()

    # Lista pra guardar widgets que mudam de cor
    widgets_tema = []

    # Logo
    caminho_imagem = resource_path(r"Imagens\nome kifome.png")
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame, image=img_tk, bg=pegar_cor("fundo"))
            label_img.pack(pady=10)
            widgets_tema.append(("bg", label_img))
        except Exception as e:
            print(f"Erro logo: {e}")

    # Texto Editar Menu
    def Editar_Menu(event=None):
        for widget in frame.winfo_children():
            widget.destroy()
        import Editar_Menu
        Editar_Menu.montar_tela(
            frame=frame,
            voltar=lambda: montar_tela(frame, voltar, janela_principal),
            janela_principal=janela_principal
        )

    texto_editar = tk.Label(
        frame,
        text="Editar Menu",
        font=("Arial", 18, "bold"),
        fg=pegar_cor("texto"),
        bg=pegar_cor("fundo"),
        cursor="hand2"
    )
    texto_editar.place(relx=0.5, rely=0.5, anchor="center")
    texto_editar.bind("<Button-1>", Editar_Menu)
    texto_editar.bind("<Enter>", lambda e: texto_editar.config(fg=pegar_cor("texto_hover"), font=("Arial", 18, "bold", "underline")))
    texto_editar.bind("<Leave>", lambda e: texto_editar.config(fg=pegar_cor("texto"), font=("Arial", 18, "bold")))
    widgets_tema.append(("fg_bg", texto_editar))

    # Botão voltar
    caminho_voltar = resource_path(r"Imagens\voltar.png")
    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)
            janela_principal.lista_imagens.append(img_voltar)

            botao_voltar = tk.Button(
                frame,
                image=img_voltar,
                command=voltar_seguro,
                borderwidth=0,
                highlightthickness=0,
                bg=pegar_cor("fundo"),
                activebackground=pegar_cor("fundo"),
                relief="flat",
                cursor="hand2"
            )
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
            widgets_tema.append(("bg_active", botao_voltar))
        except:
            botao_voltar = tk.Button(frame, text="Voltar", font=("Arial", 14),
                                     command=voltar_seguro, bg=pegar_cor("fundo"), fg=pegar_cor("texto"))
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
            widgets_tema.append(("fg_bg", botao_voltar))
    else:
        botao_voltar = tk.Button(frame, text="Voltar", font=("Arial", 14),
                                 command=voltar_seguro, bg=pegar_cor("fundo"), fg=pegar_cor("texto"))
        botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
        widgets_tema.append(("fg_bg", botao_voltar))

    # Altura janela
    altura_tela = janela_principal.winfo_height()
    if altura_tela <= 1:
        altura_tela = janela_principal.winfo_screenheight()

    # Borda branca rodapé
    altura_rodape = int(altura_tela * 0.07)
    rodape = tk.Frame(frame, bg=pegar_cor("rodape"), height=altura_rodape)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)
    widgets_tema.append(("bg", rodape))

    # Texto ALPHA VERSION
    tamanho_fonte = int(altura_tela * 0.025)
    texto = tk.Label(
        frame,
        text="ALPHA VERSION 1.0",
        bg=pegar_cor("rodape"),
        fg=pegar_cor("texto_rodape"),
        font=("Dubai", tamanho_fonte, "bold"),
        padx=0,
        pady=0
    )
    texto.place(relx=0.09, rely=0.977, anchor="center")
    widgets_tema.append(("fg_bg", texto))

    # --- BOTÃO TEMA CLARO/ESCURO ---
    def alternar_tema():
        janela_principal.tema_escuro = not janela_principal.tema_escuro
        novo_texto = "☀️ Claro" if janela_principal.tema_escuro else "🌙 Escuro"
        botao_tema.config(text=novo_texto)

        # Atualiza todas as cores
        frame.config(bg=pegar_cor("fundo"))

        for tipo, widget in widgets_tema:
            try:
                if tipo == "bg":
                    widget.config(bg=pegar_cor("fundo"))
                elif tipo == "fg_bg":
                    widget.config(fg=pegar_cor("texto"), bg=pegar_cor("fundo"))
                elif tipo == "bg_active":
                    widget.config(bg=pegar_cor("fundo"), activebackground=pegar_cor("fundo"))
            except:
                pass

        # Atualiza rodapé e texto alpha
        rodape.config(bg=pegar_cor("rodape"))
        texto.config(bg=pegar_cor("rodape"), fg=pegar_cor("texto_rodape"))

        # Atualiza hover do texto_editar
        texto_editar.bind("<Enter>", lambda e: texto_editar.config(fg=pegar_cor("texto_hover"), font=("Arial", 18, "bold", "underline")))
        texto_editar.bind("<Leave>", lambda e: texto_editar.config(fg=pegar_cor("texto"), font=("Arial", 18, "bold")))

    texto_inicial = "☀️ Claro" if janela_principal.tema_escuro else "🌙 Escuro"
    botao_tema = tk.Button(
        frame,
        text=texto_inicial,
        command=alternar_tema,
        font=("Arial", 12, "bold"),
        bg=pegar_cor("texto"),
        fg=pegar_cor("fundo"),
        bd=0,
        cursor="hand2",
        padx=15,
        pady=5
    )
    botao_tema.place(relx=0.975, rely=0.05, anchor="ne")
    widgets_tema.append(("inverter", botao_tema))