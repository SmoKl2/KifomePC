import tkinter as tk
from PIL import Image, ImageTk
import Menu
import Carrinho
import Configuracoes
import sys
import os
import sqlite3
import ctypes

myappid = 'kifome.app.v1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class Utils:
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    @staticmethod
    def pasta_app():
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.abspath(".")

class TemaManager:
    temas = {
        "claro": {
            "fundo": "#FCB57D",
            "texto": "#2c3e50",
            "rodape": "white",
            "texto_rodape": "Black"
        },
        "escuro": {
            "fundo": "#1e272e",
            "texto": "#ecf0f1",
            "rodape": "#0f1419",
            "texto_rodape": "#ecf0f1"
        }
    }

    @staticmethod
    def pegar_cor(janela_principal, chave):
        tema_atual = "escuro" if janela_principal.tema_escuro else "claro"
        return TemaManager.temas[tema_atual][chave]

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(Utils.pasta_app(), "cardapio.db"))
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                preco REAL,
                descricao TEXT,
                imagem TEXT
            )
        """)
        self.conn.commit()

    def fechar(self):
        try:
            self.conn.close()
        except:
            pass

class TelaPrincipal:
    def __init__(self, frame, voltar_callback, janela_principal):
        self.frame = frame
        self.voltar_callback = voltar_callback
        self.janela_principal = janela_principal
        self.db = Database()

        self.largura_tela = janela_principal.winfo_screenwidth()
        self.altura_tela = janela_principal.winfo_screenheight()

        self.largura_botao = int(self.largura_tela * 0.28)
        self.altura_botao = int(self.altura_tela * 0.45)

        self.inicializar_janela()
        self.limpar_frame()
        self.montar_interface()

    def inicializar_janela(self):
        if not hasattr(self.janela_principal, 'tema_escuro'):
            self.janela_principal.tema_escuro = False
        if not hasattr(self.janela_principal, 'lista_imagens'):
            self.janela_principal.lista_imagens = []

        cor_fundo = TemaManager.pegar_cor(self.janela_principal, "fundo")
        self.frame.config(bg=cor_fundo)

    def limpar_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def voltar_pro_menu(self):
        TelaPrincipal(self.frame, self.voltar_pro_menu, self.janela_principal)

    def criar_logo(self):
        caminho_imagem = Utils.resource_path(r"Imagens\nome kifome.png")
        if os.path.exists(caminho_imagem):
            try:
                img_original = Image.open(caminho_imagem).convert("RGBA")
                largura_logo = int(self.largura_tela * 0.45)
                altura_logo = int(largura_logo * 0.367)
                img_original = img_original.resize((largura_logo, altura_logo))
                img_tk = ImageTk.PhotoImage(img_original)
                self.janela_principal.lista_imagens.append(img_tk)

                cor_fundo = TemaManager.pegar_cor(self.janela_principal, "fundo")
                label_img = tk.Label(self.frame, image=img_tk, bg=cor_fundo)
                label_img.pack(pady=(self.altura_tela * 0.02, 0))
            except:
                pass

    def criar_botao_imagem(self, caminho_relativo, relx, command):
        cor_fundo = TemaManager.pegar_cor(self.janela_principal, "fundo")

        imagem_original = Image.open(Utils.resource_path(caminho_relativo))
        imagem_original = imagem_original.resize((self.largura_botao, self.altura_botao))
        imagem_botao = ImageTk.PhotoImage(imagem_original)
        self.janela_principal.lista_imagens.append(imagem_botao)

        botao = tk.Button(
            self.frame,
            image=imagem_botao,
            command=command,
            borderwidth=0,
            highlightthickness=0,
            bg=cor_fundo,
            activebackground=cor_fundo,
            relief="flat",
            cursor="hand2",
        )
        botao.place(relx=relx, rely=0.6, anchor="center")

    def abrir_menu(self):
        self.limpar_frame()
        Menu.montar_tela(self.frame, self.voltar_pro_menu, self.janela_principal)

    def abrir_carrinho(self):
        self.limpar_frame()
        Carrinho.montar_tela(self.frame, self.voltar_pro_menu, self.janela_principal)

    def abrir_config(self):
        self.limpar_frame()
        Configuracoes.montar_tela(self.frame, self.voltar_pro_menu, self.janela_principal)

    def criar_rodape(self):
        altura_tela = self.janela_principal.winfo_height()
        if altura_tela <= 1:
            altura_tela = self.janela_principal.winfo_screenheight()

        altura_rodape = int(altura_tela * 0.07)
        rodape = tk.Frame(self.frame, bg=TemaManager.pegar_cor(self.janela_principal, "rodape"),
                         height=altura_rodape)
        rodape.place(relx=0, rely=1, anchor="sw", relwidth=1)

        tamanho_fonte = int(altura_tela * 0.025)
        texto = tk.Label(
            self.frame,
            text="ALPHA VERSION 1.0",
            bg=TemaManager.pegar_cor(self.janela_principal, "rodape"),
            fg=TemaManager.pegar_cor(self.janela_principal, "texto_rodape"),
            font=("Dubai", tamanho_fonte, "bold"),
            padx=0,
            pady=0
        )
        texto.place(relx=0.09, rely=0.977, anchor="center")

    def montar_interface(self):
        self.criar_logo()
        self.criar_botao_imagem(r"Imagens\Menu.png", 0.17, self.abrir_menu)
        self.criar_botao_imagem(r"Imagens\Carrinho.png", 0.497, self.abrir_carrinho)
        self.criar_botao_imagem(r"Imagens\Configurações.png", 0.825, self.abrir_config)
        self.criar_rodape()

class App:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Kifome")

        # Estado inicial do tema
        self.janela.tema_escuro = False
        self.janela.lista_imagens = []

        cor_inicial = TemaManager.pegar_cor(self.janela, "fundo")
        self.janela.configure(bg=cor_inicial)

        self.configurar_icone()
        self.janela.state('zoomed')

        self.container = tk.Frame(self.janela, bg=cor_inicial)
        self.container.pack(fill="both", expand=True)

        self.iniciar()

    def configurar_icone(self):
        caminho_icone = Utils.resource_path("Imagens/icone.ico")
        if os.path.exists(caminho_icone):
            self.janela.iconbitmap(caminho_icone)

    def iniciar(self):
        TelaPrincipal(self.container, self.iniciar, self.janela)

    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()