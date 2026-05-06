import tkinter as tk

janela = tk.Tk()
janela.title("Tela1")
janela.geometry("1280x720")

texto = tk.Label(janela, text="Hello World")
texto.pack(pady=20)

botao = tk.Button(janela, text="Entrar", command=lambda: print("Entrou"))
botao.pack()

janela.mainloop()