import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import shutil
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

    cor_fundo = "#FCB57D"
    frame.config(bg=cor_fundo)

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

    # --- BANCO ---
    conn = sqlite3.connect("cardapio.db")
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

    # Cria pasta pra salvar as imagens dos produtos
    pasta_imagens = r"Imagens\Produtos"
    os.makedirs(pasta_imagens, exist_ok=True)

    # --- LOGO ---
    caminho_imagem = r"Imagens\nome kifome.png"
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

    # --- FORM DE CADASTRO ---
    frame_form = tk.Frame(frame, bg="#34495e", bd=2, relief="ridge")
    frame_form.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(frame_form, text="CADASTRAR PRODUTO", bg="#34495e", fg="white",
             font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

    tk.Label(frame_form, text="Nome:", bg="#34495e", fg="white", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_nome = tk.Entry(frame_form, width=30, font=("Arial", 11))
    entry_nome.grid(row=1, column=1, pady=5)

    tk.Label(frame_form, text="Preço:", bg="#34495e", fg="white", font=("Arial", 11)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_preco = tk.Entry(frame_form, width=30, font=("Arial", 11))
    entry_preco.grid(row=2, column=1, pady=5)

    tk.Label(frame_form, text="Descrição:", bg="#34495e", fg="white", font=("Arial", 11)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_descricao = tk.Entry(frame_form, width=30, font=("Arial", 11))
    entry_descricao.grid(row=3, column=1, pady=5)

    tk.Label(frame_form, text="Imagem:", bg="#34495e", fg="white", font=("Arial", 11)).grid(row=4, column=0, sticky="e", padx=5, pady=5)
    label_imagem_path = tk.Label(frame_form, text="Nenhuma imagem selecionada", bg="#34495e", fg="#95a5a6",
                                 font=("Arial", 10), width=30, anchor="w")
    label_imagem_path.grid(row=4, column=1, pady=5, sticky="w")

    caminho_imagem_selecionada = [None] # usar lista pra poder alterar dentro da função

    def escolher_imagem():
        caminho = filedialog.askopenfilename(
            title="Escolher imagem do produto",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if caminho:
            caminho_imagem_selecionada[0] = caminho
            label_imagem_path.config(text=os.path.basename(caminho), fg="white")

    tk.Button(frame_form, text="Escolher", bg="#3498db", fg="white", bd=0,
             font=("Arial", 10, "bold"), cursor="hand2", command=escolher_imagem).grid(row=4, column=2, padx=5)

    # --- CARDÁPIO ---
    frame_cardapio = tk.Frame(frame, bg="#34495e", bd=2, relief="ridge")
    frame_cardapio.pack(fill="both", expand=True, padx=20, pady=10)

    tk.Label(frame_cardapio, text="CARDÁPIO", bg="#34495e", fg="white",
             font=("Arial", 18, "bold")).pack(pady=10)

    canvas_produtos = tk.Canvas(frame_cardapio, bg="#34495e", highlightthickness=0)
    scrollbar_prod = ttk.Scrollbar(frame_cardapio, orient="vertical", command=canvas_produtos.yview)
    frame_produtos = tk.Frame(canvas_produtos, bg="#34495e")

    frame_produtos.bind("<Configure>", lambda e: canvas_produtos.configure(scrollregion=canvas_produtos.bbox("all")))
    canvas_produtos.create_window((0, 0), window=frame_produtos, anchor="nw")
    canvas_produtos.configure(yscrollcommand=scrollbar_prod.set)

    canvas_produtos.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar_prod.pack(side="right", fill="y")

    # --- FUNÇÕES ---
    def criar_card_produto(pai, id_item, nome, preco, descricao, caminho_img):
        card = tk.Frame(pai, bg="white", bd=2, relief="raised")
        card.pack(fill="x", pady=5, padx=5)

        frame_conteudo = tk.Frame(card, bg="white")
        frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

        # Imagem do produto
        if caminho_img and os.path.exists(caminho_img):
            try:
                img_prod = Image.open(caminho_img).convert("RGBA")
                img_prod = img_prod.resize((100, 100))
                img_prod_tk = ImageTk.PhotoImage(img_prod)
                janela_principal.lista_imagens.append(img_prod_tk)
                tk.Label(frame_conteudo, image=img_prod_tk, bg="white").pack(side="left", padx=(0, 15))
            except:
                pass

        # Textos
        frame_textos = tk.Frame(frame_conteudo, bg="white")
        frame_textos.pack(side="left", fill="both", expand=True)

        tk.Label(frame_textos, text=nome, bg="white", fg="#2c3e50",
                font=("Arial", 16, "bold"), anchor="w").pack(fill="x")

        tk.Label(frame_textos, text=descricao, bg="white", fg="#7f8c8d",
                font=("Arial", 11), anchor="w", wraplength=600).pack(fill="x", pady=(5, 0))

        tk.Label(frame_textos, text=f"R$ {preco:.2f}", bg="white", fg="#27ae60",
                font=("Arial", 18, "bold"), anchor="w").pack(fill="x", pady=(10, 0))

        # Botão deletar
        def deletar():
            if messagebox.askyesno("Deletar", f"Deletar {nome}?"):
                cursor.execute("DELETE FROM produtos WHERE id=?", (id_item,))
                conn.commit()
                # Apaga imagem se existir
                if caminho_img and os.path.exists(caminho_img):
                    try:
                        os.remove(caminho_img)
                    except:
                        pass
                carregar_produtos()

        tk.Button(frame_conteudo, text="X", bg="#e74c3c", fg="white", bd=0,
                 font=("Arial", 10, "bold"), cursor="hand2", command=deletar).pack(side="right")

    def carregar_produtos():
        for widget in frame_produtos.winfo_children():
            widget.destroy()

        cursor.execute("SELECT id, nome, preco, descricao, imagem FROM produtos ORDER BY nome")
        produtos = cursor.fetchall()

        if not produtos:
            tk.Label(frame_produtos, text="Nenhum produto cadastrado",
                    bg="#34495e", fg="#7f8c8d", font=("Arial", 14)).pack(pady=50)
        else:
            for prod in produtos:
                criar_card_produto(frame_produtos, prod[0], prod[1], prod[2], prod[3], prod[4])

    def adicionar_produto():
        nome = entry_nome.get().strip()
        preco = entry_preco.get().strip()
        descricao = entry_descricao.get().strip()

        if not nome or not preco:
            messagebox.showerror("Erro", "Preencha nome e preço")
            return

        try:
            preco_float = float(preco.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido")
            return

        caminho_final = None
        if caminho_imagem_selecionada[0]:
            # Copia imagem pra pasta do projeto com nome único
            extensao = os.path.splitext(caminho_imagem_selecionada[0])[1]
            nome_arquivo = f"{nome.replace(' ', '_')}_{len(os.listdir(pasta_imagens))}{extensao}"
            caminho_final = os.path.join(pasta_imagens, nome_arquivo)
            shutil.copy2(caminho_imagem_selecionada[0], caminho_final)

        cursor.execute("INSERT INTO produtos (nome, preco, descricao, imagem) VALUES (?,?,?,?)",
                       (nome, preco_float, descricao, caminho_final))
        conn.commit()

        # Limpa campos
        entry_nome.delete(0, "end")
        entry_preco.delete(0, "end")
        entry_descricao.delete(0, "end")
        label_imagem_path.config(text="Nenhuma imagem selecionada", fg="#95a5a6")
        caminho_imagem_selecionada[0] = None

        carregar_produtos()
        messagebox.showinfo("Sucesso", "Produto adicionado!")

    tk.Button(frame_form, text="ADICIONAR PRODUTO", bg="#27ae60", fg="white", bd=0,
             font=("Arial", 12, "bold"), cursor="hand2", command=adicionar_produto).grid(row=5, column=0, columnspan=3, pady=15)

    # --- BOTÃO VOLTAR ---
    def Configuracoes():
        conn.close()
        for widget in frame.winfo_children():
            widget.destroy()
        frame.tkraise()
        caminho = r"Configuracoes.py"
        try:
            if "Configuracoes" in sys.modules:
                del sys.modules["Configuracoes"]
            spec = importlib.util.spec_from_file_location("Configuracoes", caminho)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            modulo.montar_tela(frame=frame, voltar=lambda: frame.tkraise(), janela_principal=janela_principal)
        except Exception as e:
            tk.Label(frame, text=f"Erro: {e}", fg="red", bg=cor_fundo).pack()

    caminho_voltar = r"Imagens\voltar.png"
    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)
            janela_principal.lista_imagens.append(img_voltar)

            botao_voltar = tk.Button(
                frame, image=img_voltar, command=Configuracoes,
                borderwidth=0, highlightthickness=0, bg=cor_fundo,
                activebackground=cor_fundo, relief="flat", cursor="hand2"
            )
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
        except:
            tk.Button(frame, text="Voltar", command=Configuracoes).place(relx=0.025, rely=0.05)
    else:
        tk.Button(frame, text="Voltar", command=Configuracoes).place(relx=0.025, rely=0.05)

    # Rodapé
    rodape = tk.Frame(frame, bg="white", height=55)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

    texto = tk.Label(
        frame, text="ALPHA VERSION 1.0 - CARDÁPIO", bg="white", fg="Black",
        font=("Dubai", 20, "bold"), padx=0, pady=0
    )
    texto.place(relx=0.07, rely=0.977, anchor="center")

    carregar_produtos()