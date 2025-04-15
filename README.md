# 💬 Aplicação Web de Mensagens em Python (Sem Frameworks)

Este projeto é uma aplicação web simples desenvolvida sem o uso de frameworks, utilizando apenas Python puro e o paradigma procedural. O objetivo é registrar, visualizar e excluir mensagens, armazenadas em um arquivo `.txt`.

---

## 🛠 Tecnologias Utilizadas

### Back-end
- Python 3.x (sem frameworks)
- Módulos padrão: http.server, os, urllib, datetime

### Front-end
- HTML5
- CSS3 (responsivo)
- JavaScript (para interações dinâmicas e atalhos de teclado)

---

## 📁 Estrutura do Projeto

visitas/
│
├── static/
│   ├── scripts.js
│   └── style.css
│
├── mensagens.py
├── pagina.py
├── requirements.txt
├── server.py

---

## ▶️ Como Executar

1. Certifique-se de que o Python 3 está instalado.
2. (Opcional) Ative o ambiente virtual dentro da pasta `.venv`.
3. Rode o servidor com:

   python server.py

4. Acesse no navegador:

   http://localhost:8000

---

## 📝 Funcionalidades

- Visualização de todas as mensagens
- Registro de novas mensagens com data e hora
- Exclusão individual de mensagens
- Interface responsiva com HTML/CSS/JS
- Criação automática do arquivo de mensagens se não existir
- Atalho de teclado (Shift + Q) para encerrar o servidor sem fechar o terminal

---

## 🧪 Requisitos

- Python 3.x
- Nenhuma biblioteca externa é necessária.
- Tudo é feito com módulos padrão do Python.

---

## 🔐 Encerramento com Atalho de Teclado

O JavaScript escuta a tecla `Shift + Q` e envia uma requisição ao servidor, que interpreta isso como um sinal para encerramento limpo da aplicação.

---

## 📄 Licença

Este projeto está disponível sob a licença MIT. Fique à vontade para estudar, adaptar ou compartilhar!
