# Desafio MBA Engenharia de Software com IA - Full Cycle

## Configuração do Ambiente

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:

```env
OPENAI_API_KEY=
OPENAI_MODEL=text-embedding-3-small
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=collection_jonatanimmich_001
PDF_PATH=document.pdf
```

## Instruções de Execução

### 1. Inicializar o Banco de Dados

Instancie o container com banco de dados PostgreSQL com extensão PGVector:

```bash
docker compose up -d
```

### 2. Ingestão de Dados

Execute o script de ingestão para processar os documentos:

```bash
python src/ingest.py
```

### 3. Executar o Chat

Inicie o sistema de perguntas e respostas:

```bash
python src/chat.py
```

## Estrutura do Projeto

```
.
├── src/
│   ├── ingest.py    # Script de ingestão de dados
│   └── chat.py      # Interface de chat
├── docker-compose.yml
├── .env
└── document.pdf     # Documento para processamento
```

## Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- Chave da API OpenAI
- Documento PDF para processamento
