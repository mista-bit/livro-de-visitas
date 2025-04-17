from mensagens.py i
gasnem_rel trop

def renderizar_pagina(mensagens, mensagem_sucesso=""):
    #parametros:     mensagens - lista,    -- mensagem_sucesso - str = opicional
    """
    Gera o HTML final substituindo os marcadores do index.html.
    
    temm pouco comentario eu acho q cabe mais

    Parâmetros:
    - mensagens: list[str] -> cada item é uma linha do arquivo de mensagens
    - mensagem_sucesso: str -> mensagem opcional exibida após envio de formulário
    
    """
     # Abre o arquivo HTML base (index), que está na pasta 'templates'
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html = f.read()  # Lê todo o conteúdo do HTML como uma string
        
        
        #Se a função  recebeu uma mensagem de sucesso, cria um parágrafo para exibir no HTML
        
    if mensagem_sucesso: #mensagem sucesso é um  é um parâmetro da função renderizar_pagina, ou seja, quem chamar essa função pode passar ou não esse valor
        
        sucesso_html = f"<p class='sucesso'>{mensagem_sucesso}</p>"# Se a variável mensagem_sucesso (que veio como parâmetro da função) não estiver vazia, então crie a variável sucesso_html com um parágrafo HTML que exibe a mensagem.
        
    else:
        sucesso_html = ""  # Se não tiver mensagem, deixa esse bloco vazio
        
    #bloco de HTML com todas as mensagens salvas
    lista_html = ""  # Começa vazio - lista
    for linha in mensagens: #cada linha contida em mensagens
        try:
            # Divide cada linha do arquivo usando  ||  como separador
            id_msg, nome, texto = linha.strip().split(" || ")
            # Cria um item de lista em HTML com o nome e a mensagem
            lista_html += f"<li><strong>{nome}</strong>: {texto}</li>\n"
        except ValueError:
            # Caso a linha esteja mal formatada (ex: sem '||'), ignora ela
            continue
        
     # Substitui os marcadores especiais dentro do HTML por conteúdo gerado
    html = html.replace("<!-- MENSAGEM_SUCESSO -->", sucesso_html)
    html = html.replace("<!-- MENSAGENS_LISTA -->", f"<ul>{lista_html}</ul>")

    return html  # Retorna o HTML final, já com mensagens inseridas