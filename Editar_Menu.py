import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import shutil
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

def abrir_detalhe(id_item, nome, preco, descricao, caminho_img):
    pass

def montar_tela(frame, voltar, janela_principal):
    for widget in frame.winfo_children():
        widget.destroy()

    cor_fundo = "#FCB57D"
    cor_cardapio = "#FCB57D"

    frame.config(bg=cor_fundo)

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

#Banco
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
        canvas_tela.unbind_all("<MouseWheel>")
        canvas_tela.unbind_all("<Button-4>")
        canvas_tela.unbind_all("<Button-5>")
        try:
            conn.close()
        except:
            pass
        voltar()

#Criar pasta pra salvar as imagens dos produtos
    pasta_imagens = os.path.join(pasta_app(), "Imagens", "Produtos")
    os.makedirs(pasta_imagens, exist_ok=True)

#Rolagem de tela
    canvas_tela = tk.Canvas(frame, bg=cor_fundo, highlightthickness=0)
    scrollbar_tela = ttk.Scrollbar(frame, orient="vertical", command=canvas_tela.yview)
    frame_conteudo = tk.Frame(canvas_tela, bg=cor_fundo)

    frame_conteudo.bind("<Configure>", lambda e: canvas_tela.configure(scrollregion=canvas_tela.bbox("all")))
    canvas_window = canvas_tela.create_window((0, 0), window=frame_conteudo, anchor="n")
    canvas_tela.configure(yscrollcommand=scrollbar_tela.set)

    def centralizar(event):
        largura_canvas = canvas_tela.winfo_width()
        canvas_tela.coords(canvas_window, int(largura_canvas * 0.35), 0)
        canvas_tela.itemconfig(canvas_window, width=min(1000, largura_canvas - 40))

    canvas_tela.bind("<Configure>", centralizar)
    canvas_tela.pack(side="left", fill="both", expand=True)
    scrollbar_tela.pack(side="right", fill="y")


    def _on_mousewheel(event):
        canvas_tela.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas_tela.bind_all("<MouseWheel>", _on_mousewheel)
    canvas_tela.bind_all("<Button-4>", lambda e: canvas_tela.yview_scroll(-1, "units"))
    canvas_tela.bind_all("<Button-5>", lambda e: canvas_tela.yview_scroll(1, "units"))

#Código nome kifome
    caminho_imagem = resource_path(r"Imagens\nome kifome.png")
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame_conteudo, image=img_tk, bg=cor_fundo)
            label_img.pack(pady=(80, 10))
        except Exception as e:
            print(f"Erro logo: {e}")

#Form de cadastro
    frame_form = tk.Frame(frame_conteudo, bg="#34495e", bd=2, relief="ridge")
    frame_form.pack(fill="x", pady=(0, 10))

    tk.Label(frame_form, text="CADASTRAR PRODUTO", bg="#34495e", fg="white",
             font=("Arial", 16, "bold")).grid(row=0, columnspan=3, pady=10)

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

    caminho_imagem_selecionada = [None]

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

#Cardápio
    frame_cardapio = tk.Frame(frame_conteudo, bg="#34495e", bd=2, relief="ridge")
    frame_cardapio.pack(fill="both", expand=True, pady=10)

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

#Funções
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

    def criar_card_produto(pai, id_item, nome, preco, descricao, caminho_img):
        card = tk.Frame(pai, bg="white", bd=2, relief="raised", cursor="hand2")
        card.pack(fill="x", pady=8, padx=5)

        def ao_clicar(e):
            abrir_detalhe(id_item, nome, preco, descricao, caminho_img)

        card.bind("<Button-1>", ao_clicar)
        card.bind("<Enter>", lambda e: card.config(bg="#f8f9fa"))
        card.bind("<Leave>", lambda e: card.config(bg="white"))

        frame_conteudo_card = tk.Frame(card, bg="white", cursor="hand2")
        frame_conteudo_card.pack(fill="both", expand=True, padx=15, pady=15)
        frame_conteudo_card.bind("<Button-1>", ao_clicar)

        if caminho_img and os.path.exists(caminho_img):
            try:
                img_prod = Image.open(caminho_img).convert("RGBA")
                img_prod = img_prod.resize((120, 120))
                img_prod_tk = ImageTk.PhotoImage(img_prod)
                janela_principal.lista_imagens.append(img_prod_tk)
                label_img = tk.Label(frame_conteudo_card, image=img_prod_tk, bg="white", cursor="hand2")
                label_img.pack(side="left", padx=(0, 20))
                label_img.bind("<Button-1>", ao_clicar)
            except:
                pass

        frame_textos = tk.Frame(frame_conteudo_card, bg="white", cursor="hand2")
        frame_textos.pack(side="left", fill="both", expand=True)
        frame_textos.bind("<Button-1>", ao_clicar)

        label_nome = tk.Label(frame_textos, text=nome, bg="white", fg="#2c3e50",
                font=("Arial", 18, "bold"), anchor="w", cursor="hand2")
        label_nome.pack(fill="x")
        label_nome.bind("<Button-1>", ao_clicar)

        label_desc = tk.Label(frame_textos, text=descricao, bg="white", fg="#7f8c8d",
                font=("Arial", 12), anchor="w", wraplength=600, justify="left", cursor="hand2")
        label_desc.pack(fill="x", pady=(8, 0))
        label_desc.bind("<Button-1>", ao_clicar)

        frame_baixo = tk.Frame(frame_textos, bg="white", cursor="hand2")
        frame_baixo.pack(fill="x", pady=(12, 0))
        frame_baixo.bind("<Button-1>", ao_clicar)

        label_preco = tk.Label(frame_baixo, text=f"R$ {preco:.2f}", bg="white", fg="#27ae60",
                font=("Arial", 22, "bold"), cursor="hand2")
        label_preco.pack(side="left")
        label_preco.bind("<Button-1>", ao_clicar)

        frame_botoes = tk.Frame(frame_baixo, bg="white")
        frame_botoes.pack(side="right")

#Botão deletar produto
        def deletar_produto():
            if messagebox.askyesno("Deletar", f"Deletar {nome} do cardápio?\n\nIsso vai remover o produto permanentemente!"):
                try:
                    cursor.execute("DELETE FROM produtos WHERE id=?", (id_item,))
                    conn.commit()
                    if caminho_img and os.path.exists(caminho_img):
                        try:
                            os.remove(caminho_img)
                        except:
                            pass
                    carregar_produtos()
                    messagebox.showinfo("Sucesso", f"{nome} deletado do cardápio!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao deletar: {e}")

        btn_deletar = tk.Button(frame_botoes, text="X", bg="#c0392b", fg="white", bd=0,
                 font=("Arial", 12, "bold"), cursor="hand2", command=deletar_produto, width=3)
        btn_deletar.pack(side="left", padx=3, ipady=5)

#Barra de Pesquisa
    frame_pesquisa = tk.Frame(frame_conteudo, bg=cor_fundo)
    frame_pesquisa.pack(fill="x", padx=20, pady=(0, 10), before=frame_form)

    tk.Label(frame_pesquisa, text="Pesquisar:", bg=cor_fundo, fg="#2c3e50",
             font=("Arial", 12, "bold")).pack(side="left", padx=(0, 10))

    entry_pesquisa = tk.Entry(frame_pesquisa, font=("Arial", 12), width=40)
    entry_pesquisa.pack(side="left", fill="x", expand=True, ipady=5)

    def pesquisar(event=None):
        termo = entry_pesquisa.get().strip()
        carregar_produtos(termo)

    entry_pesquisa.bind("<KeyRelease>", pesquisar)

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
            extensao = os.path.splitext(caminho_imagem_selecionada[0])[1]
            nome_arquivo = f"{nome.replace(' ', '_')}_{len(os.listdir(pasta_imagens))}{extensao}"
            caminho_final = os.path.join(pasta_imagens, nome_arquivo)
            shutil.copy2(caminho_imagem_selecionada[0], caminho_final)

        cursor.execute("INSERT INTO produtos (nome, preco, descricao, imagem) VALUES (?,?,?,?)",
                       (nome, preco_float, descricao, caminho_final))
        conn.commit()

        entry_nome.delete(0, "end")
        entry_preco.delete(0, "end")
        entry_descricao.delete(0, "end")
        label_imagem_path.config(text="Nenhuma imagem selecionada", fg="#95a5a6")
        caminho_imagem_selecionada[0] = None

        carregar_produtos()
        messagebox.showinfo("Sucesso", "Produto adicionado!")

    tk.Button(frame_form, text="ADICIONAR PRODUTO", bg="#27ae60", fg="white", bd=0,
             font=("Arial", 12, "bold"), cursor="hand2", command=adicionar_produto).grid(row=5, column=0, columnspan=3, pady=15)

    tk.Label(frame_conteudo, text="", bg=cor_fundo).pack(pady=40)

#Código botão voltar
    caminho_voltar = resource_path(r"Imagens\voltar.png")
    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)
            janela_principal.lista_imagens.append(img_voltar)

            botao_voltar = tk.Label(
                frame,
                image=img_voltar,
                bg=cor_fundo,
                cursor="hand2"
            )
            botao_voltar.image = img_voltar
            botao_voltar.bind("<Button-1>", lambda e: voltar_seguro())
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
            botao_voltar.lift()
        except:
            botao_voltar = tk.Button(frame, text="Voltar", font=("Arial", 14), command=voltar_seguro)
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
            botao_voltar.lift()
    else:
        botao_voltar = tk.Button(frame, text="Voltar", font=("Arial", 14), command=voltar_seguro)
        botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
        botao_voltar.lift()

#Altura janela
    altura_tela = janela_principal.winfo_height()
    if altura_tela <= 1:
        altura_tela = janela_principal.winfo_screenheight()

#Borda branca rodapé
    altura_rodape = int(altura_tela * 0.07)
    rodape = tk.Frame(frame, bg="white", height=altura_rodape)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

#Texto ALPHA VERSION
    tamanho_fonte = int(altura_tela * 0.025)
    texto = tk.Label(
        frame,
        text="ALPHA VERSION 1.0",
        bg="#FEFEFE",
        fg="Black",
        font=("Dubai", tamanho_fonte, "bold"),
        padx=0,
        pady=0
    )
    texto.place(relx=0.09, rely=0.977, anchor="center")

    carregar_produtos()