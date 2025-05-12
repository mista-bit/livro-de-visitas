# Livro de Visitas Web - Python Puro

Servidor web completo para livro de visitas desenvolvido com Python padrão (sem frameworks).

## Estrutura do Projeto

```
livro-visitas/
│
├── static/
│   └── style.css          # Arquivo de estilos CSS
│
├── templates/
│   └── index.html         # Template HTML base
│
├── mensagens.py           # Lógica de manipulação das mensagens
├── pagina.py              # Gerador de páginas HTML
├── server.py              # Servidor HTTP principal
└── README.md              # Documentação do projeto
```

## Como Usar

1. Clone o repositório:

2. Inicie o servidor:
```bash
python server.py
```

3. Acesse no navegador:
```
http://localhost:8080
```

## Funcionalidades Principais

- **Backend**:
  - Servidor HTTP implementado com sockets Python
  - Sistema completo de CRUD para mensagens
  - Armazenamento persistente em arquivo texto

- **Frontend**:
  - Interface limpa e responsiva
  - Formulário para envio de mensagens
  - Visualização e exclusão de mensagens

## Arquivos Principais

- `server.py`: Implementação do servidor web
- `mensagens.py`: Manipulação do arquivo de mensagens
- `pagina.py`: Geração do HTML dinâmico
- `templates/index.html`: Template base da aplicação
- `static/style.css`: Estilos da aplicação

## Requisitos

- Python 3.6 ou superior
- Nenhuma dependência externa necessária

## Licença

MIT License - Consulte o arquivo [LICENSE](LICENSE) para detalhes.
