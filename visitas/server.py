import socket
import os
from urllib.parse import parse_qs
from mensagens import salvar_mensagem, apagar_mensagem, ler_mensagens
from pagina import renderizar_pagina

HOST = 'localhost'
PORT = 8080

def extrair_requisicao_http(conexao):
    dados = b""
    conexao.settimeout(5)  # Tempo de espera de 5 segundos para receber dados
    while True:
        try:
            parte = conexao.recv(1024)
            if not parte:
                print("⚠️ Conexão fechada pelo cliente.")
                break  # Sai do loop se não houver dados (conexão fechada)
            dados += parte
            print(f"🔍 Dados recebidos: {parte}")
            if b"\r\n\r\n" in dados:
                break
        except socket.timeout:
            print("⚠️ Timeout atingido enquanto aguardava dados da requisição.")
            break
        except Exception as e:
            print(f"❌ Erro ao ler a requisição: {e}")
            break

    headers, _, restante = dados.partition(b"\r\n\r\n")
    headers_str = headers.decode("utf-8")
    print("\n📥 Cabeçalhos recebidos:\n", headers_str)

    if not headers_str.strip():
        print("❌ Cabeçalho da requisição vazio!")
        return None, None  # Retorna None se não houver cabeçalhos

    return headers_str, restante

def receber_corpo(headers, conexao, body_inicial):
    content_length = 0
    for linha in headers.split("\r\n"):
        if linha.lower().startswith("content-length:"):
            content_length = int(linha.split(":")[1].strip())
            break
    print(f"📏 Content-Length esperado: {content_length}")
    restante = body_inicial
    while len(restante) < content_length:
        restante += conexao.recv(1024)
    corpo = restante.decode("utf-8")
    print("📦 Corpo da requisição recebido:\n", corpo)
    return corpo

def tratar_requisicao(headers, body_raw):
    if not headers:  # Se não houver cabeçalho, retorna um erro 400
        return "HTTP/1.1 400 Bad Request\r\n\r\nCabeçalho não encontrado.".encode("utf-8")
    
    linha_requisicao = headers.splitlines()[0]
    metodo, caminho, _ = linha_requisicao.split()

    print(f"\n➡️ Método: {metodo} | Caminho: {caminho}")

    if caminho.startswith("/static/"):
        caminho_arquivo = os.path.join(os.path.dirname(__file__), caminho.lstrip("/"))
        print(f"🗂️ Servindo arquivo estático: {caminho_arquivo}")
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "rb") as f:
                conteudo = f.read()
            return b"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n" + conteudo
        else:
            print("❌ Arquivo estático não encontrado.")
            return b"HTTP/1.1 404 Not Found\r\n\r\n" + "Arquivo estático não encontrado.".encode("utf-8")

    if metodo == "GET":
        print("🔎 GET recebido. Carregando mensagens...")
        html = renderizar_pagina(ler_mensagens())  # Renderiza sempre as mensagens mais recentes
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nCache-Control: no-cache\r\n\r\n{html}".encode("utf-8")

    if metodo == "POST":
        dados = parse_qs(body_raw)
        print("📝 POST recebido com dados:", dados)

        if caminho == "/":
            nome = dados.get("nome", [""])[0]
            mensagem = dados.get("mensagem", [""])[0]
            if nome and mensagem:
                print(f"💾 Salvando mensagem de {nome}: {mensagem}")
                salvar_mensagem(nome, mensagem)
                html = renderizar_pagina(ler_mensagens(), "Mensagem enviada com sucesso!")
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nCache-Control: no-cache\r\n\r\n{html}".encode("utf-8")

        elif caminho == "/delete":
            id_msg = dados.get("id", [""])[0]
            if id_msg:
                print(f"🗑️ Apagando mensagem com ID: {id_msg}")
                apagar_mensagem(id_msg)
                html = renderizar_pagina(ler_mensagens(), "Mensagem apagada com sucesso!")
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nCache-Control: no-cache\r\n\r\n{html}".encode("utf-8")

    print("❗ Requisição não reconhecida.")
    return "HTTP/1.1 400 Bad Request\r\n\r\nRequisição não reconhecida.".encode("utf-8")

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"🚀 Servidor rodando em http://{HOST}:{PORT}")

        while True:
            conexao, endereco = s.accept()
            print(f"\n🔌 Nova conexão de {endereco}")
            with conexao:
                headers, body_inicial = extrair_requisicao_http(conexao)
                if not headers:
                    print("❌ Requisição inválida.")
                    continue  # Ignora requisições inválidas

                if "POST" in headers:
                    body = receber_corpo(headers, conexao, body_inicial)
                else:
                    body = ""
                resposta = tratar_requisicao(headers, body)
                conexao.sendall(resposta)
                print("✅ Resposta enviada.\n")

if __name__ == "__main__":
    iniciar_servidor()
