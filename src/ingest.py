import os
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    from pathlib import Path
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_core.documents import Document
    from langchain_postgres import PGVector

    if not PDF_PATH:
        raise RuntimeError("A variável de ambiente PDF_PATH não está definida.")

    pdf_path = Path(PDF_PATH)
    if not pdf_path.exists():
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")

    docs = PyPDFLoader(str(pdf_path)).load()

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False
    ).split_documents(docs)
    if not splits:
        print("Nenhum split gerado a partir do PDF.")
        return

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)
    print(f"{len(enriched)} documentos inseridos no banco vetorial.")


if __name__ == "__main__":
    ingest_pdf()