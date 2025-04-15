import os
from datetime import datetime

mensagens = r"visitas\mensagens.txt"

def checar_arquivo():
    if not os.path.exists(mensagens):
        with open(mensagens, 'w', encoding="utf-8") as arquivo:
            pass
        print("Arquivo criado com sucesso.")

checar_arquivo()
