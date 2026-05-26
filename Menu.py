import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import carrinho_global
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

    cor_fundo = "#FCB57D"
    cor_cardapio = "#FCB57D"

    frame.config(bg=cor_fundo)

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

    # --- BANCO ---
    conn = sqlite3.connect(resource_path("cardapio.db")) # CORRIGIDO
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

    # --- FECHA O BANCO ANTES DE VOLTAR ---
    def voltar_seguro():
        try:
            conn.close()
        except:
            pass
        voltar()

    # --- FRAME TOPO PRA SEGURAR O BOTÃO ---
    frame_topo = tk.Frame(frame, bg=cor_fundo)
    frame_topo.pack(side="top", fill="x")

    # --- BOTÃO VOLTAR CORRIGIDO ---

    caminho_voltar = resource_path(r"Imagens\voltar.png") # CORRIGIDO
    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)
            janela_principal.lista_imagens.append(img_voltar)

            botao_voltar = tk.Button(
                frame_topo, # PAI É O FRAME_TOPO
                image=img_voltar,
                command=voltar_seguro, # USA VOLTAR_SEGURO
                borderwidth=0,
                highlightthickness=0,
                bg=cor_fundo,
                activebackground=cor_fundo,
                relief="flat",
                cursor="hand2"
            )
            botao_voltar.image = img_voltar
            botao_voltar.pack(side="left", padx=10, pady=10) # PACK EM VEZ DE PLACE
        except Exception as e:
            print(f"Erro botão: {e}")
            tk.Button(frame_topo, text="Voltar", command=voltar_seguro).pack(side="left", padx=10, pady=10)
    else:
        tk.Button(frame_topo, text="Voltar", command=voltar_seguro).pack(side="left", padx=10, pady=10)

    # --- LOGO ---
    caminho_imagem = resource_path(r"Imagens\nome kifome.png") # CORRIGIDO
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((400, 150))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame, image=img_tk, bg=cor_fundo)
            label_img.pack(pady=10)
        except:
            pass

    # --- BARRA DE PESQUISA ---
    frame_pesquisa = tk.Frame(frame, bg=cor_fundo)
    frame_pesquisa.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(frame_pesquisa, text="Pesquisar:", bg=cor_fundo, fg="#2c3e50",
             font=("Arial", 12, "bold")).pack(side="left", padx=(0, 10))

    entry_pesquisa = tk.Entry(frame_pesquisa, font=("Arial", 12), width=40)
    entry_pesquisa.pack(side="left", fill="x", expand=True, ipady=5)

    # --- CARDÁPIO ---
    frame_cardapio = tk.Frame(frame, bg=cor_cardapio, bd=2, relief="ridge")
    frame_cardapio.pack(fill="both", expand=True, padx=20, pady=10)

    canvas_produtos = tk.Canvas(frame_cardapio, bg=cor_cardapio, highlightthickness=0)
    scrollbar_prod = ttk.Scrollbar(frame_cardapio, orient="vertical", command=canvas_produtos.yview)
    frame_produtos = tk.Frame(canvas_produtos, bg=cor_cardapio)

    frame_produtos.bind("<Configure>", lambda e: canvas_produtos.configure(scrollregion=canvas_produtos.bbox("all")))
    canvas_produtos.create_window((0, 0), window=frame_produtos, anchor="nw")
    canvas_produtos.configure(yscrollcommand=scrollbar_prod.set)

    canvas_produtos.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar_prod.pack(side="right", fill="y")

    # --- FUNÇÕES ---
    def criar_card_produto(pai, id_item, nome, preco, descricao, caminho_img):
        card = tk.Frame(pai, bg="white", bd=2, relief="raised")
        card.pack(fill="x", pady=8, padx=5)

        frame_conteudo = tk.Frame(card, bg="white")
        frame_conteudo.pack(fill="both", expand=True, padx=15, pady=15)

        # Imagem do produto - CORRIGIDO
        if caminho_img:
            caminho_img_abs = resource_path(caminho_img)
            if os.path.exists(caminho_img_abs):
                try:
                    img_prod = Image.open(caminho_img_abs).convert("RGBA")
                    img_prod = img_prod.resize((120, 120))
                    img_prod_tk = ImageTk.PhotoImage(img_prod)
                    janela_principal.lista_imagens.append(img_prod_tk)
                    tk.Label(frame_conteudo, image=img_prod_tk, bg="white").pack(side="left", padx=(0, 20))
                except:
                    pass

        # Textos
        frame_textos = tk.Frame(frame_conteudo, bg="white")
        frame_textos.pack(side="left", fill="both", expand=True)

        tk.Label(frame_textos, text=nome, bg="white", fg="#2c3e50",
                font=("Arial", 18, "bold"), anchor="w").pack(fill="x")

        tk.Label(frame_textos, text=descricao, bg="white", fg="#7f8c8d",
                font=("Arial", 12), anchor="w", wraplength=600, justify="left").pack(fill="x", pady=(8, 0))

        frame_baixo = tk.Frame(frame_textos, bg="white")
        frame_baixo.pack(fill="x", pady=(12, 0))

        tk.Label(frame_baixo, text=f"R$ {preco:.2f}", bg="white", fg="#27ae60",
                font=("Arial", 22, "bold")).pack(side="left")

        # Botões adicionar e remover
        frame_botoes = tk.Frame(frame_baixo, bg="white")
        frame_botoes.pack(side="right")

        def adicionar():
            carrinho_global.adicionar_item(id_item, nome, preco)
            messagebox.showinfo("Adicionado", f"{nome} adicionado ao carrinho!")

        def remover():
            carrinho_global.remover_item(id_item)
            messagebox.showinfo("Removido", f"{nome} removido do carrinho!")

        tk.Button(frame_botoes, text="REMOVER", bg="#e74c3c", fg="white", bd=0,
                 font=("Arial", 10, "bold"), cursor="hand2", command=remover).pack(side="left", padx=3, ipady=5)

        tk.Button(frame_botoes, text="ADICIONAR", bg="#27ae60", fg="white", bd=0,
                 font=("Arial", 10, "bold"), cursor="hand2", command=adicionar).pack(side="left", padx=3, ipady=5)

    def carregar_produtos(filtro=""):
        for widget in frame_produtos.winfo_children():
            widget.destroy()

        if filtro:
            cursor.execute("""
                SELECT id, nome, preco, descricao, imagem
                FROM produtos
                WHERE nome LIKE? OR descricao LIKE?
                ORDER BY nome
            """, (f"%{filtro}%", f"%{filtro}%"))
        else:
            cursor.execute("SELECT id, nome, preco, descricao, imagem FROM produtos ORDER BY nome")

        produtos = cursor.fetchall()

        if not produtos:
            texto = "Nenhum produto encontrado" if filtro else "Nenhum produto cadastrado"
            tk.Label(frame_produtos, text=texto,
                    bg=cor_cardapio, fg="#7f8c8d", font=("Arial", 16)).pack(pady=50)
        else:
            for prod in produtos:
                criar_card_produto(frame_produtos, prod[0], prod[1], prod[2], prod[3], prod[4])

    def pesquisar(event=None):
        termo = entry_pesquisa.get().strip()
        carregar_produtos(termo)

    entry_pesquisa.bind("<KeyRelease>", pesquisar)

    # Borda branca rodapé
    rodape = tk.Frame(frame, bg="white", height=55)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

    # Texto ALPHA VERSION
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

    carregar_produtos()