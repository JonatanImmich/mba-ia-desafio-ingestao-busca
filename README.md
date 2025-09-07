# Desafio MBA Engenharia de Software com IA - Full Cycle
Definir variaveis de ambiente .env 
   
   OPENAI_API_KEY=
   OPENAI_MODEL=text-embedding-3-small
   PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
   PGVECTOR_COLLECTION=collection_jonatanimmich_001
   PDF_PATH=document.pdf
   
1. Instanciar container com banco de dados postgres com extensão PGVector
   docker compose up -d

2. Fazer Ingestão de dados
   python src/ingest.py

3. Rodar chat de perguntas
   python src/chat.py

   

   
