import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import carrinho_global
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

    # --- LOGO ---
    caminho_imagem = r"Imagens\nome kifome.png"
    if os.path.exists(caminho_imagem):
        try:
            img_original = Image.open(caminho_imagem).convert("RGBA")
            img_original = img_original.resize((600, 220))
            img_tk = ImageTk.PhotoImage(img_original)
            janela_principal.lista_imagens.append(img_tk)
            label_img = tk.Label(frame, image=img_tk, bg=cor_fundo)
            label_img.place(relx=0.5, rely=0.16, anchor="center")
        except Exception as e:
            label_img = tk.Label(frame, text=f"Erro ao carregar imagem: {e}", fg="red", bg=cor_fundo)
            label_img.place(relx=0.5, rely=0.16, anchor="center")
    else:
        label_img = tk.Label(frame, text="Imagem não encontrada", fg="red", bg=cor_fundo)
        label_img.place(relx=0.5, rely=0.16, anchor="center")

    # --- CARRINHO ---
    frame_carrinho = tk.Frame(frame, bg="#2c3e50", bd=2, relief="ridge")
    frame_carrinho.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.85, relheight=0.55)

    tk.Label(frame_carrinho, text="MEU CARRINHO", bg="#2c3e50", fg="white",
             font=("Arial", 20, "bold")).pack(pady=15)

    canvas_carrinho = tk.Canvas(frame_carrinho, bg="#2c3e50", highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame_carrinho, orient="vertical", command=canvas_carrinho.yview)
    frame_itens = tk.Frame(canvas_carrinho, bg="#2c3e50")

    frame_itens.bind("<Configure>", lambda e: canvas_carrinho.configure(scrollregion=canvas_carrinho.bbox("all")))
    canvas_carrinho.create_window((0, 0), window=frame_itens, anchor="nw")
    canvas_carrinho.configure(yscrollcommand=scrollbar.set)

    canvas_carrinho.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    # --- FUNÇÕES ---
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

    # Total
    frame_total = tk.Frame(frame, bg="#27ae60", height=70)
    frame_total.place(relx=0.5, rely=0.85, anchor="center", relwidth=0.85)
    frame_total.pack_propagate(False)

    label_total = tk.Label(frame_total, text=f"TOTAL: R$ {carrinho_global.get_total():.2f}",
                          bg="#27ae60", fg="white", font=("Arial", 24, "bold"))
    label_total.pack(expand=True)

    def atualizar_total():
        label_total.config(text=f"TOTAL: R$ {carrinho_global.get_total():.2f}")

    # Botões de ação
    frame_botoes = tk.Frame(frame, bg=cor_fundo)
    frame_botoes.place(relx=0.5, rely=0.93, anchor="center", relwidth=0.85)

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

    # Botão voltar
    caminho_voltar = r"Imagens\voltar.png"
    if os.path.exists(caminho_voltar):
        try:
            img_voltar_original = Image.open(caminho_voltar).convert("RGBA")
            img_voltar_original = img_voltar_original.resize((60, 60))
            img_voltar = ImageTk.PhotoImage(img_voltar_original)
            janela_principal.lista_imagens.append(img_voltar)

            botao_voltar = tk.Button(
                frame,
                image=img_voltar,
                command=voltar,
                borderwidth=0,
                highlightthickness=0,
                bg=cor_fundo,
                activebackground=cor_fundo,
                relief="flat",
                cursor="hand2"
            )
            botao_voltar.image = img_voltar
            botao_voltar.place(relx=0.025, rely=0.05, anchor="center")
        except:
            tk.Button(frame, text="Voltar", command=voltar).place(relx=0.025, rely=0.05)
    else:
        tk.Button(frame, text="Voltar", command=voltar).place(relx=0.025, rely=0.05)

    # Rodapé
    rodape = tk.Frame(frame, bg="white", height=55)
    rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

    texto = tk.Label(
        frame,
        text="ALPHA VERSION 1.0 - CARRINHO",
        bg="white",
        fg="Black",
        font=("Dubai", 20, "bold"),
        padx=0,
        pady=0
    )
    texto.place(relx=0.07, rely=0.977, anchor="center")

    atualizar_carrinho()