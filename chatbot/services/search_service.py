
from .rag_service import embedding_model, collection


def search_chunks(question, document_id, top_k=3):

    # Step 1: Validate question
    question = question.strip()

    if not question:
        return []

    # Step 2: Get chunks belonging to selected PDF
    stored_data = collection.get(
        where={
            "document_id": int(document_id)
        },
        include=["metadatas"]
    )

    total_chunks = len(stored_data["ids"])

    if total_chunks == 0:
        return []

    # Step 3: Convert question into embedding
    question_embedding = embedding_model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    # Step 4: Search relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, total_chunks),
        where={
            "document_id": int(document_id)
        },
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    # Step 5: Extract results
    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for text, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_chunks.append({
            "text": text,
            "page_number": metadata["page_number"],
            "document_id": metadata["document_id"],
            "distance": distance
        })

    return retrieved_chunks
