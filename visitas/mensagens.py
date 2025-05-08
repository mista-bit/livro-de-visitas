import os
from datetime import datetime

mensagens = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mensagens.txt")
def gerar_id():
    """Gera um ID único baseado na data e hora atual."""
    return datetime.now().strftime("%Y%m%d%H%M%S")

def checar_arquivo():
    if not os.path.exists(mensagens):
        with open(mensagens, 'w', encoding="utf-8") as arquivo:
            pass
        print("Arquivo criado com sucesso.")

def ler_mensagens():
    """Lê as mensagens salvas no arquivo."""
    checar_arquivo()
    with open(mensagens, 'r', encoding="utf-8") as arquivo:
        return arquivo.readlines()

def salvar_mensagem(nome, mensagem):
    """Salva uma mensagem no arquivo com um ID baseado na hora."""
    checar_arquivo()
    id_mensagem = gerar_id()
    linha = f"{id_mensagem} || {nome} || {mensagem}\n"
    with open(mensagens, 'a', encoding="utf-8") as arquivo:
        arquivo.write(linha)
    print("Mensagem salva com sucesso.")
    
def apagar_mensagem(id_mensagem):
    """Apaga uma mensagem do arquivo."""
    checar_arquivo()
    mensagens_existentes = ler_mensagens()
    with open(mensagens, 'w', encoding="utf-8") as arquivo:
        for linha in mensagens_existentes:
            if not linha.split(" || ")[0] == id_mensagem:
                arquivo.write(linha)
    print("Mensagem apagada com sucesso.")
