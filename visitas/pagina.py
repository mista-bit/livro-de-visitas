from mensagens import ler_mensagens
import os

def renderizar_pagina(mensagens, mensagem_sucesso=""):
    """
    Gera o HTML final substituindo os marcadores do index.html.
    """
    css_path = "/static/style.css"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "templates", "index.html")

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    bloco_sucesso = f"<p><strong>{mensagem_sucesso}</strong></p>" if mensagem_sucesso else ""
    html = html.replace("<!-- MENSAGEM_SUCESSO -->", bloco_sucesso)

    lista_html = []
    for linha in mensagens:
        try:
            id_msg, nome, texto = linha.strip().split(" || ")
            lista_html.append(f"""
                <div class="mensagem">
                    <p><strong>{nome}</strong>: {texto}</p>
                    <form method="POST" action="/delete">
                        <input type="hidden" name="id" value="{id_msg}">
                        <button type="submit">Apagar Mensagem</button>
                    </form>
                </div>
            """)
        except ValueError:
            continue

    html = html.replace("<!-- MENSAGENS_LISTA -->", f"<ul>{''.join(lista_html)}</ul>")
    html = html.replace("<!-- CSS para estilizacao -->", f'<link rel="stylesheet" href="{css_path}">')

    return html

print(renderizar_pagina(ler_mensagens()))
