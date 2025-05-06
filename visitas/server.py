import socket
import os
from urllib.parse import parse_qs
from mensagens import salvar_mensagem, apagar_mensagem, ler_mensagens
from pagina import renderizar_pagina

HOST = 'localhost'
PORT = 8080

def extrair_requisicao_http(conexao):
    dados = b""
    while True:
        parte = conexao.recv(1024)
        dados += parte
        if b"\r\n\r\n" in dados:
            break
    headers, _, restante = dados.partition(b"\r\n\r\n")
    headers_str = headers.decode("utf-8")
    return headers_str, restante

def receber_corpo(headers, conexao, body_inicial):
    content_length = 0
    for linha in headers.split("\r\n"):
        if linha.lower().startswith("content-length:"):
            content_length = int(linha.split(":")[1].strip())
            break
    restante = body_inicial
    while len(restante) < content_length:
        restante += conexao.recv(1024)
    return restante.decode("utf-8")

def tratar_requisicao(headers, body_raw):
    linha_requisicao = headers.splitlines()[0]
    metodo, caminho, _ = linha_requisicao.split()

    if caminho.startswith("/static/"):
        caminho_arquivo = caminho.lstrip("/")
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "rb") as f:
                conteudo = f.read()
            resposta = b"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n" + conteudo
            return resposta
        else:
            return b"HTTP/1.1 404 Not Found\r\n\r\n" + "Arquivo estático não encontrado.".encode("utf-8")

    if metodo == "GET":
        html = renderizar_pagina(ler_mensagens())
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html}".encode("utf-8")

    if metodo == "POST":
        dados = parse_qs(body_raw)

        if caminho == "/":
            nome = dados.get("nome", [""])[0]
            mensagem = dados.get("mensagem", [""])[0]
            if nome and mensagem:
                salvar_mensagem(nome, mensagem)
                html = renderizar_pagina(ler_mensagens(), "Mensagem enviada com sucesso!")
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html}".encode("utf-8")

        elif caminho == "/delete":
            id_msg = dados.get("id", [""])[0]
            if id_msg:
                apagar_mensagem(id_msg)
                html = renderizar_pagina(ler_mensagens(), "Mensagem apagada com sucesso!")
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html}".encode("utf-8")

    return "HTTP/1.1 400 Bad Request\r\n\r\nRequisição não reconhecida.".encode("utf-8")

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Servidor rodando em http://{HOST}:{PORT}")

        while True:
            conexao, _ = s.accept()
            with conexao:
                headers, body_inicial = extrair_requisicao_http(conexao)
                if "POST" in headers:
                    body = receber_corpo(headers, conexao, body_inicial)
                else:
                    body = ""
                resposta = tratar_requisicao(headers, body)
                conexao.sendall(resposta)

if __name__ == "__main__":
    iniciar_servidor()