import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pasta temporária do PyInstaller
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

carrinho = []

def adicionar_item(id_item, nome, preco):
    for item in carrinho:
        if item['id'] == id_item:
            item['qtd'] += 1
            return
    carrinho.append({'id': id_item, 'nome': nome, 'preco': preco, 'qtd': 1})

def remover_item(id_item):
    for idx, item in enumerate(carrinho):
        if item['id'] == id_item:
            if item['qtd'] > 1:
                item['qtd'] -= 1
            else:
                carrinho.pop(idx)
            return

def limpar_carrinho():
    carrinho.clear()

def get_total():
    return sum(item['preco'] * item['qtd'] for item in carrinho)