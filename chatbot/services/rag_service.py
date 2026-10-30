
import chromadb

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


# Initialize embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="pdf_documents"
)


def process_pdf_pages(document_id, pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    documents = []
    metadatas = []
    ids = []

    for page in pages:

        text = page["text"]

        if not text:
            continue

        chunks = splitter.split_text(text)

        for index, chunk in enumerate(chunks):

            documents.append(chunk)

            metadatas.append({
                "document_id": document_id,
                "page_number": page["page_number"]
            })

            ids.append(
                f"pdf_{document_id}_page_{page['page_number']}_chunk_{index}"
            )

    if not documents:
        return 0

    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(documents)
