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
    frame.config(bg=cor_fundo)

    if not hasattr(janela_principal, 'lista_imagens'):
        janela_principal.lista_imagens = []

#Banco
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
        canvas_tela.unbind_all("<MouseWheel>")
        canvas_tela.unbind_all("<Button-4>")
        canvas_tela.unbind_all("<Button-5>")
        try:
            conn.close()
        except:
            pass
        voltar()

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

#Código botão voltar
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
                bg="#FCB57D",
                activebackground="#FCB57D",
                relief="flat",
                cursor="hand2"
            )
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
        except:
            botao_voltar = tk.Button(frame, text="Voltar", font=("Arial", 14),
                                     command=voltar_seguro)
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
    else:
        botao_voltar = tk.Button(frame, text="Voltar", font=("Arial", 14), command=voltar_seguro)
        botao_voltar.place(relx=0.025, rely=0.05, anchor="center")

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

#Carrinho
    frame_carrinho = tk.Frame(frame_conteudo, bg="#2c3e50", bd=2, relief="ridge")
    frame_carrinho.pack(pady=20, fill="x", ipady=10)

    tk.Label(frame_carrinho, text="MEU CARRINHO", bg="#2c3e50", fg="white",
             font=("Arial", 20, "bold")).pack(pady=15)

    canvas_carrinho = tk.Canvas(frame_carrinho, bg="#2c3e50", highlightthickness=0, height=300)
    scrollbar_itens = ttk.Scrollbar(frame_carrinho, orient="vertical", command=canvas_carrinho.yview)
    frame_itens = tk.Frame(canvas_carrinho, bg="#2c3e50")

    frame_itens.bind("<Configure>", lambda e: canvas_carrinho.configure(scrollregion=canvas_carrinho.bbox("all")))
    canvas_carrinho.create_window((0, 0), window=frame_itens, anchor="nw")
    canvas_carrinho.configure(yscrollcommand=scrollbar_itens.set)

    canvas_carrinho.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar_itens.pack(side="right", fill="y")

#Funções
    def atualizar_carrinho():
        for widget in frame_itens.winfo_children():
            widget.destroy()

        if not carrinho_global.carrinho:
            tk.Label(frame_itens, text="Carrinho vazio",
                    bg="#2c3e50", fg="#95a5a6", font=("Arial", 16)).pack(pady=50)
        else:
            for item in carrinho_global.carrinho:
                card = tk.Frame(frame_itens, bg="#34495e", bd=2, relief="raised")
                card.pack(fill="x", pady=5, padx=10)

                frame_info = tk.Frame(card, bg="#34495e")
                frame_info.pack(fill="x", padx=15, pady=15)

                tk.Label(frame_info, text=f"{item['qtd']}x", bg="#34495e", fg="#f39c12",
                        font=("Arial", 18, "bold")).pack(side="left", padx=(0, 15))

                frame_textos = tk.Frame(frame_info, bg="#34495e")
                frame_textos.pack(side="left", fill="x", expand=True)

                tk.Label(frame_textos, text=item['nome'], bg="#34495e", fg="white",
                        font=("Arial", 16, "bold"), anchor="w").pack(fill="x")

                subtotal = item['preco'] * item['qtd']
                tk.Label(frame_textos, text=f"R$ {subtotal:.2f}", bg="#34495e", fg="#2ecc71",
                        font=("Arial", 14, "bold"), anchor="w").pack(fill="x")

                frame_botoes_item = tk.Frame(frame_info, bg="#34495e")
                frame_botoes_item.pack(side="right")

                def remover_um(id_item=item['id']):
                    carrinho_global.remover_item(id_item)
                    atualizar_carrinho()
                    atualizar_total()

                tk.Button(frame_botoes_item, text="−", bg="#e74c3c", fg="white", bd=0,
                         font=("Arial", 12, "bold"), cursor="hand2", width=3,
                         command=remover_um).pack(side="left", padx=2)

                def adicionar_um(id_item=item['id'], nome=item['nome'], preco=item['preco']):
                    carrinho_global.adicionar_item(id_item, nome, preco)
                    atualizar_carrinho()
                    atualizar_total()

                tk.Button(frame_botoes_item, text="+", bg="#27ae60", fg="white", bd=0,
                         font=("Arial", 12, "bold"), cursor="hand2", width=3,
                         command=adicionar_um).pack(side="left", padx=2)

#Total
    frame_total = tk.Frame(frame_conteudo, bg="#27ae60", height=70)
    frame_total.pack(pady=10, fill="x")
    frame_total.pack_propagate(False)

    label_total = tk.Label(frame_total, text=f"TOTAL: R$ {carrinho_global.get_total():.2f}",
                          bg="#27ae60", fg="white", font=("Arial", 24, "bold"))
    label_total.pack(expand=True)

    def atualizar_total():
        label_total.config(text=f"TOTAL: R$ {carrinho_global.get_total():.2f}")

#Botões de ação
    frame_botoes = tk.Frame(frame_conteudo, bg=cor_fundo)
    frame_botoes.pack(pady=10, fill="x")

    def finalizar():
        if not carrinho_global.carrinho:
            messagebox.showwarning("Vazio", "Carrinho vazio")
            return
        total = carrinho_global.get_total()
        resumo = "\n".join([f"{i['qtd']}x {i['nome']} - R$ {i['preco'] * i['qtd']:.2f}" for i in carrinho_global.carrinho])
        if messagebox.askyesno("Finalizar Venda", f"Confirmar venda?\n\n{resumo}\n\nTOTAL: R$ {total:.2f}"):
            carrinho_global.limpar_carrinho()
            atualizar_carrinho()
            atualizar_total()
            messagebox.showinfo("Sucesso", "Venda finalizada!")

    def limpar():
        if carrinho_global.carrinho and messagebox.askyesno("Limpar", "Limpar carrinho?"):
            carrinho_global.limpar_carrinho()
            atualizar_carrinho()
            atualizar_total()

    tk.Button(frame_botoes, text="FINALIZAR", bg="#27ae60", fg="white",
             font=("Arial", 14, "bold"), cursor="hand2", command=finalizar).pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=8)

    tk.Button(frame_botoes, text="LIMPAR", bg="#e74c3c", fg="white",
             font=("Arial", 14, "bold"), cursor="hand2", command=limpar).pack(side="right", expand=True, fill="x", padx=(5, 0), ipady=8)

#Altura janela
    altura_tela = janela_principal.winfo_height()
    if altura_tela <= 1:
        altura_tela = janela_principal.winfo_screenheight()

    altura_rodape = int(altura_tela * 0.07)
    tk.Label(frame_conteudo, text="", bg=cor_fundo, height=int(altura_rodape/10)).pack()

#Borda branca rodapé
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

    atualizar_carrinho()