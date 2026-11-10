# Parte 1 - Questão 1: GPT-2

## Como executar

Use Python 3.11 ou 3.12. Dentro desta pasta, crie um ambiente e instale as dependências:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
# Linux ou macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
python -m pip install -r requirements.txt
uvicorn main:app --port 8000
```

Abra http://127.0.0.1:8000/docs, selecione POST /generate, clique em “Try it out” e envie:

```json
{"text": "Once upon a time"}
```

Também é possível enviar pelo terminal (no Windows, use curl.exe):

```bash
curl -X POST http://127.0.0.1:8000/generate -H "Content-Type: application/json" -d '{"text":"Once upon a time"}'
```

Execute uma aplicação por vez na porta 8000. Textos vazios são recusados com erro 422.

O primeiro início baixa o modelo do Hugging Face e precisa de internet. Depois, os pesos ficam no cache. A execução utiliza CPU.

A resposta tem o campo `generated_text`, com a entrada e sua continuação. O modelo gera até 60 tokens novos. Entradas que ultrapassem a janela do modelo são recusadas.
