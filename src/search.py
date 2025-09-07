import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    try:
        
        # Configurar embeddings e banco de dados vetorial
        embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

        # Conexão com PGVector
        db = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PGVECTOR_COLLECTION"),
            connection=os.getenv("PGVECTOR_URL"),
            use_jsonb=True,
        )
      
        # 1. Vetorizar a pergunta.
        # 2. Buscar os 10 resultados mais relevantes (k=10) no banco vetorial.
        # A pergunta é automaticamente vetorizada pelo PGVector
        results = db.similarity_search_with_score(question, k=10)

        # Filtrar apenas resultados com boa similaridade
        score_threshold=0.8
        filtered_results = [
            (doc, score) for doc, score in results 
            if score <= score_threshold  # scores menores = maior similaridade
        ]
        
        if not filtered_results:
            print(f"Nenhum resultado encontrado com similaridade suficiente (threshold: {score_threshold})")
            return None
        
        # 5. COMBINAR CONTEXTO DOS RESULTADOS
        combined_content = " ".join([
            f"[Score: {score:.4f}, Fonte: {doc.metadata.get('source', 'N/A')}] {doc.page_content}" 
            for doc, score in filtered_results
        ])

        # Montar o prompt
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        messages = prompt.format_messages(contexto=combined_content, pergunta=question)
        
        # Chamar a LLM
        model = ChatOpenAI(model="gpt-5-nano", temperature=0.1)
        message = model.invoke(messages)

        # Retornar a resposta ao usuário.
        print(message.content)
        
    except Exception as e:
        print(f"Erro ao inicializar a busca: {e}")
        return None

