import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- BANCO ---
conn = sqlite3.connect("cardapio.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        preco REAL,
        categoria TEXT
    )
""")
conn.commit()


# --- FUNÇÕES ---
def adicionar():
    nome = entry_nome.get()
    preco = entry_preco.get()
    categoria = combo_cat.get()

    if nome == "" or preco == "":
        messagebox.showerror("Erro", "Preencha nome e preço")
        return

    try:
        cursor.execute("INSERT INTO produtos (nome, preco, categoria) VALUES (?, ?, ?)",
                       (nome, float(preco), categoria))
        conn.commit()
        limpar()
        atualizar_tabela()
        messagebox.showinfo("Sucesso", "Item adicionado")
    except ValueError:
        messagebox.showerror("Erro", "Preço inválido")


def atualizar_tabela():
    for item in tabela.get_children():
        tabela.delete(item)
    cursor.execute("SELECT * FROM produtos ORDER BY id DESC")
    for row in cursor.fetchall():
        tabela.insert("", "end", values=row)


def limpar():
    entry_nome.delete(0, "end")
    entry_preco.delete(0, "end")
    combo_cat.set("Lanche")


# --- TELA ---
root = tk.Tk()
root.title("PDV Cardápio")
root.geometry("600x500")
root.configure(bg="#2c3e50")

# Form
frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
frame.pack(pady=10, fill="x", padx=10)

tk.Label(frame, text="Nome:", bg="#34495e", fg="white").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(frame, width=30, font=("Arial", 11))
entry_nome.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Preço:", bg="#34495e", fg="white").grid(row=1, column=0, sticky="w")
entry_preco = tk.Entry(frame, width=30, font=("Arial", 11))
entry_preco.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Categoria:", bg="#34495e", fg="white").grid(row=2, column=0, sticky="w")
combo_cat = ttk.Combobox(frame, values=["Lanche", "Bebida", "Sobremesa", "Porção"], width=28)
combo_cat.grid(row=2, column=1, pady=5)
combo_cat.set("Lanche")

tk.Button(frame, text="Adicionar", bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
          command=adicionar, cursor="hand2").grid(row=3, column=0, columnspan=2, pady=10)

# Tabela
tabela = ttk.Treeview(root, columns=("ID", "Nome", "Preço", "Categoria"), show="headings")
tabela.heading("ID", text="ID")
tabela.heading("Nome", text="Nome")
tabela.heading("Preço", text="Preço R$")
tabela.heading("Categoria", text="Categoria")
tabela.column("ID", width=50)
tabela.column("Preço", width=80)
tabela.pack(pady=10, padx=10, fill="both", expand=True)

atualizar_tabela()
root.mainloop()
conn.close()