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

def pasta_app():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.abspath(".")

def montar_tela(frame, voltar, janela_principal):
    for widget in frame.winfo_children():
        widget.destroy()

#SISTEMA DE TEMAS
    if not hasattr(janela_principal, 'tema_escuro'):
        janela_principal.tema_escuro = False

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

    temas = {
        "claro": {
            "fundo": "#FCB57D",
            "cardapio": "#FCB57D",
            "texto": "#2c3e50",
            "texto_sec": "#7f8c8d",
            "card": "white",
            "card_hover": "#f8f9fa",
            "verde": "#27ae60",
            "azul": "#3498db",
            "vermelho": "#e74c3c",
            "rodape": "white",
            "texto_rodape": "Black",
            "canvas": "#FCB57D"
        },
        "escuro": {
            "fundo": "#1e272e",
            "cardapio": "#2c3e50",
            "texto": "#ecf0f1",
            "texto_sec": "#95a5a6",
            "card": "#34495e",
            "card_hover": "#3d566e",
            "verde": "#2ecc71",
            "azul": "#3498db",
            "vermelho": "#e74c3c",
            "rodape": "#0f1419",
            "texto_rodape": "#ecf0f1",
            "canvas": "#2c3e50"
        }
    }

    def pegar_cor(chave):
        tema_atual = "escuro" if janela_principal.tema_escuro else "claro"
        return temas[tema_atual][chave]

    cor_fundo = pegar_cor("fundo")
    cor_cardapio = pegar_cor("cardapio")

    frame.config(bg=cor_fundo)

    # Banco
    caminho_banco = os.path.join(pasta_app(), "cardapio.db")
    conn = sqlite3.connect(caminho_banco)
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

    frame_topo = tk.Frame(frame, bg=cor_fundo)
    frame_topo.pack(side="top", fill="x")

    # Botão voltar
    caminho_voltar = resource_path(r"Imagens\voltar.png")
    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)
            janela_principal.lista_imagens.append(img_voltar)

            botao_voltar = tk.Label(
                frame_topo,
                image=img_voltar,
                bg=cor_fundo,
                cursor="hand2"
            )
            botao_voltar.image = img_voltar
            botao_voltar.bind("<Button-1>", lambda e: voltar_seguro())
            botao_voltar.pack(side="left", padx=10, pady=10)
        except:
            tk.Button(frame_topo, text="Voltar", command=voltar_seguro,
                     bg=pegar_cor("card"), fg=pegar_cor("texto")).pack(side="left", padx=10, pady=10)
    else:
        tk.Button(frame_topo, text="Voltar", command=voltar_seguro,
                 bg=pegar_cor("card"), fg=pegar_cor("texto")).pack(side="left", padx=10, pady=10)

    # Logo kifome
    caminho_imagem = resource_path(r"Imagens\nome kifome.png")
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame, image=img_tk, bg=cor_fundo)
            label_img.pack(pady=(0, 5))
        except:
            pass

    # Barra de Pesquisa
    frame_pesquisa = tk.Frame(frame, bg=cor_fundo)
    frame_pesquisa.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(frame_pesquisa, text="Pesquisar:", bg=cor_fundo, fg=pegar_cor("texto"),
             font=("Arial", 12, "bold")).pack(side="left", padx=(0, 10))

    entry_pesquisa = tk.Entry(frame_pesquisa, font=("Arial", 12), width=40,
                              bg=pegar_cor("card"), fg=pegar_cor("texto"), insertbackground=pegar_cor("texto"))
    entry_pesquisa.pack(side="left", fill="x", expand=True, ipady=5)

    # Cardápio
    frame_cardapio = tk.Frame(frame, bg=cor_cardapio, bd=2, relief="ridge")
    frame_cardapio.pack(fill="both", expand=True, padx=20, pady=10)

    canvas_produtos = tk.Canvas(frame_cardapio, bg=pegar_cor("canvas"), highlightthickness=0)
    scrollbar_prod = ttk.Scrollbar(frame_cardapio, orient="vertical", command=canvas_produtos.yview)
    frame_produtos = tk.Frame(canvas_produtos, bg=pegar_cor("canvas"))

    frame_produtos.bind("<Configure>", lambda e: canvas_produtos.configure(scrollregion=canvas_produtos.bbox("all")))
    canvas_produtos.create_window((0, 0), window=frame_produtos, anchor="nw")
    canvas_produtos.configure(yscrollcommand=scrollbar_prod.set)

    canvas_produtos.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar_prod.pack(side="right", fill="y")

    # Tela de Zoom nos itens
    def abrir_detalhe(id_item, nome, preco, descricao, caminho_img):
        for widget in frame.winfo_children():
            widget.destroy()

        cor_fundo_detalhe = pegar_cor("fundo")
        frame.config(bg=cor_fundo_detalhe)

        frame_topo_detalhe = tk.Frame(frame, bg=cor_fundo_detalhe)
        frame_topo_detalhe.pack(side="top", fill="x")

        # Botão voltar tela zoom
        caminho_voltar = resource_path(r"Imagens\voltar.png")
        if os.path.exists(caminho_voltar):
            try:
                img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
                img_voltar_original = img_voltar_original.resize((60, 60))
                img_voltar = ImageTk.PhotoImage(img_voltar_original)
                janela_principal.lista_imagens.append(img_voltar)

                btn_voltar = tk.Label(
                    frame_topo_detalhe,
                    image=img_voltar,
                    bg=cor_fundo_detalhe,
                    cursor="hand2"
                )
                btn_voltar.image = img_voltar
                btn_voltar.pack(side="left", padx=20, pady=20)
            except Exception as e:
                print(f"Erro botão voltar: {e}")
                btn_voltar = tk.Button(frame_topo_detalhe, text="← VOLTAR", bg=pegar_cor("vermelho"), fg="white",
                                       font=("Arial", 14, "bold"), cursor="hand2",
                                       command=lambda: montar_tela(frame, voltar, janela_principal))
                btn_voltar.pack(side="left", padx=20, pady=20)
        else:
            btn_voltar = tk.Button(frame_topo_detalhe, text="← VOLTAR", bg=pegar_cor("vermelho"), fg="white",
                                   font=("Arial", 14, "bold"), cursor="hand2",
                                   command=lambda: montar_tela(frame, voltar, janela_principal))
            btn_voltar.pack(side="left", padx=20, pady=20)

        canvas_detalhe = tk.Canvas(frame, bg=cor_fundo_detalhe, highlightthickness=0)
        scrollbar_detalhe = ttk.Scrollbar(frame, orient="vertical", command=canvas_detalhe.yview)

        container = tk.Frame(canvas_detalhe, bg=cor_fundo_detalhe)

        container.bind("<Configure>", lambda e: canvas_detalhe.configure(scrollregion=canvas_detalhe.bbox("all")))
        canvas_window = canvas_detalhe.create_window((0, 0), window=container, anchor="n")
        canvas_detalhe.configure(yscrollcommand=scrollbar_detalhe.set)

        def centralizar(event):
            largura_canvas = event.width
            canvas_detalhe.itemconfig(canvas_window, width=largura_canvas)
            canvas_detalhe.coords(canvas_window, largura_canvas/2, 0)

        canvas_detalhe.bind("<Configure>", centralizar)

        canvas_detalhe.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar_detalhe.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas_detalhe.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas_detalhe.bind_all("<MouseWheel>", _on_mousewheel)
        canvas_detalhe.bind_all("<Button-4>", lambda e: canvas_detalhe.yview_scroll(-1, "units"))
        canvas_detalhe.bind_all("<Button-5>", lambda e: canvas_detalhe.yview_scroll(1, "units"))

        def sair_detalhe():
            canvas_detalhe.unbind_all("<MouseWheel>")
            canvas_detalhe.unbind_all("<Button-4>")
            canvas_detalhe.unbind_all("<Button-5>")
            montar_tela(frame, voltar, janela_principal)

        btn_voltar.bind("<Button-1>", lambda e: sair_detalhe())

        frame_central = tk.Frame(container, bg=cor_fundo_detalhe)
        frame_central.pack(expand=True)

        # Imagem zoom grande
        if caminho_img and os.path.exists(caminho_img):
            try:
                img_prod = Image.open(caminho_img).convert("RGBA")
                img_prod = img_prod.resize((500, 500))
                img_prod_tk = ImageTk.PhotoImage(img_prod)
                janela_principal.lista_imagens.append(img_prod_tk)
                tk.Label(frame_central, image=img_prod_tk, bg=cor_fundo_detalhe).pack(pady=20)
            except:
                pass

        # Nome
        tk.Label(frame_central, text=nome, bg=cor_fundo_detalhe, fg=pegar_cor("texto"),
                font=("Arial", 32, "bold")).pack(pady=10)

        # Descrição
        tk.Label(frame_central, text=descricao, bg=cor_fundo_detalhe, fg=pegar_cor("texto"),
                font=("Arial", 16), wraplength=800, justify="center").pack(pady=15)

        # Preço
        tk.Label(frame_central, text=f"R$ {preco:.2f}", bg=cor_fundo_detalhe, fg=pegar_cor("verde"),
                font=("Arial", 40, "bold")).pack(pady=20)

        # Botões
        frame_botoes = tk.Frame(frame_central, bg=cor_fundo_detalhe)
        frame_botoes.pack(pady=20)

        def adicionar():
            carrinho_global.adicionar_item(id_item, nome, preco)
            messagebox.showinfo("Adicionado", f"{nome} adicionado ao carrinho!")

        def remover():
            carrinho_global.remover_item(id_item)
            messagebox.showinfo("Removido", f"{nome} removido do carrinho!")

        tk.Button(frame_botoes, text="− REMOVER", bg=pegar_cor("vermelho"), fg="white", bd=0,
                 font=("Arial", 16, "bold"), cursor="hand2", command=remover,
                 width=15, height=2).pack(side="left", padx=10)

        tk.Button(frame_botoes, text="+ ADICIONAR", bg=pegar_cor("verde"), fg="white", bd=0,
                 font=("Arial", 16, "bold"), cursor="hand2", command=adicionar,
                 width=15, height=2).pack(side="left", padx=10)

        tk.Label(frame_central, text="", bg=cor_fundo_detalhe).pack(pady=30)

    # Funções
    def get_qtd_item(id_item):
        for item in carrinho_global.carrinho:
            if item['id'] == id_item:
                return item['qtd']
        return 0

    def criar_card_produto(pai, id_item, nome, preco, descricao, caminho_img):
        card = tk.Frame(pai, bg=pegar_cor("card"), bd=2, relief="raised", cursor="hand2")
        card.pack(fill="x", pady=8, padx=5)

        def ao_clicar(e):
            abrir_detalhe(id_item, nome, preco, descricao, caminho_img)

        card.bind("<Button-1>", ao_clicar)
        card.bind("<Enter>", lambda e: card.config(bg=pegar_cor("card_hover")))
        card.bind("<Leave>", lambda e: card.config(bg=pegar_cor("card")))

        frame_conteudo = tk.Frame(card, bg=pegar_cor("card"), cursor="hand2")
        frame_conteudo.pack(fill="both", expand=True, padx=15, pady=15)
        frame_conteudo.bind("<Button-1>", ao_clicar)

        # Imagem produto
        if caminho_img and os.path.exists(caminho_img):
            try:
                img_prod = Image.open(caminho_img).convert("RGBA")
                img_prod = img_prod.resize((120, 120))
                img_prod_tk = ImageTk.PhotoImage(img_prod)
                janela_principal.lista_imagens.append(img_prod_tk)
                label_img = tk.Label(frame_conteudo, image=img_prod_tk, bg=pegar_cor("card"), cursor="hand2")
                label_img.pack(side="left", padx=(0, 20))
                label_img.bind("<Button-1>", ao_clicar)
            except:
                pass

        frame_textos = tk.Frame(frame_conteudo, bg=pegar_cor("card"), cursor="hand2")
        frame_textos.pack(side="left", fill="both", expand=True)
        frame_textos.bind("<Button-1>", ao_clicar)

        label_nome = tk.Label(frame_textos, text=nome, bg=pegar_cor("card"), fg=pegar_cor("texto"),
                font=("Arial", 18, "bold"), anchor="w", cursor="hand2")
        label_nome.pack(fill="x")
        label_nome.bind("<Button-1>", ao_clicar)

        label_desc = tk.Label(frame_textos, text=descricao, bg=pegar_cor("card"), fg=pegar_cor("texto_sec"),
                font=("Arial", 12), anchor="w", wraplength=600, justify="left", cursor="hand2")
        label_desc.pack(fill="x", pady=(8, 0))
        label_desc.bind("<Button-1>", ao_clicar)

        frame_baixo = tk.Frame(frame_textos, bg=pegar_cor("card"), cursor="hand2")
        frame_baixo.pack(fill="x", pady=(12, 0))
        frame_baixo.bind("<Button-1>", ao_clicar)

        label_preco = tk.Label(frame_baixo, text=f"R$ {preco:.2f}", bg=pegar_cor("card"), fg=pegar_cor("verde"),
                font=("Arial", 22, "bold"), cursor="hand2")
        label_preco.pack(side="left")
        label_preco.bind("<Button-1>", ao_clicar)

        # Carrinho
        label_qtd = tk.Label(frame_baixo, text=f"Qtd: {get_qtd_item(id_item)}", bg=pegar_cor("card"), fg=pegar_cor("azul"),
                font=("Arial", 16, "bold"), cursor="hand2")
        label_qtd.pack(side="left", padx=15)
        label_qtd.bind("<Button-1>", ao_clicar)

        frame_botoes = tk.Frame(frame_baixo, bg=pegar_cor("card"))
        frame_botoes.pack(side="right")

        def atualizar_qtd():
            label_qtd.config(text=f"Qtd: {get_qtd_item(id_item)}")

        def adicionar(e=None):
            carrinho_global.adicionar_item(id_item, nome, preco)
            atualizar_qtd()
            messagebox.showinfo("Adicionado", f"{nome} adicionado ao carrinho!")

        def remover(e=None):
            carrinho_global.remover_item(id_item)
            atualizar_qtd()
            messagebox.showinfo("Removido", f"{nome} removido do carrinho!")

        btn_remover = tk.Button(frame_botoes, text="REMOVER", bg=pegar_cor("vermelho"), fg="white", bd=0,
                 font=("Arial", 10, "bold"), cursor="hand2", command=remover)
        btn_remover.pack(side="left", padx=3, ipady=5)

        btn_add = tk.Button(frame_botoes, text="ADICIONAR", bg=pegar_cor("verde"), fg="white", bd=0,
                 font=("Arial", 10, "bold"), cursor="hand2", command=adicionar)
        btn_add.pack(side="left", padx=3, ipady=5)

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
                    bg=pegar_cor("canvas"), fg=pegar_cor("texto_sec"), font=("Arial", 16)).pack(pady=50)
        else:
            for prod in produtos:
                criar_card_produto(frame_produtos, prod[0], prod[1], prod[2], prod[3], prod[4])

    def pesquisar(event=None):
        termo = entry_pesquisa.get().strip()
        carregar_produtos(termo)

    entry_pesquisa.bind("<KeyRelease>", pesquisar)

    # Altura janela
    altura_tela = janela_principal.winfo_height()
    if altura_tela <= 1:
        altura_tela = janela_principal.winfo_screenheight()

    # Borda branca rodapé
    altura_rodape = int(altura_tela * 0.07)
    rodape = tk.Frame(frame, bg=pegar_cor("rodape"), height=altura_rodape)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

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

    carregar_produtos()