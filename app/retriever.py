import chromadb

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder,
)


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "nexla_docs"


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


try:
    collection = client.get_collection(
        COLLECTION_NAME
    )

except:
    raise Exception(
        "Collection not found. Run ingestion first using: python -m app.ingest"
    )


def retrieve_context(query, top_k=5):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    # -----------------------------
    # RERANKING
    # -----------------------------

    pairs = [(query, doc) for doc in docs]

    scores = reranker.predict(pairs)

    ranked_results = sorted(
        zip(scores, docs, metas),
        reverse=True,
        key=lambda x: x[0]
    )

    contexts = []

    seen = set()

    for score, doc, meta in ranked_results:

        key = (meta["source"], meta["page"])

        if key in seen:
            continue

        seen.add(key)

        contexts.append(
            {
                "content": doc,
                "source": meta["source"],
                "page": meta["page"],
                "score": float(score),
            }
        )

    print("\nRetrieved Contexts:\n")

    for c in contexts:
        print(
            f"{c['source']} | page {c['page']} | rerank score: {c['score']:.4f}"
        )

    return contexts[:3]