import os
import fitz
import chromadb
import nltk

from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer


nltk.download("punkt")
nltk.download("punkt_tab")

CHROMA_PATH = "chroma_db"
PDF_DIR = "data/pdfs"
COLLECTION_NAME = "nexla_docs"


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


client = chromadb.PersistentClient(path=CHROMA_PATH)


# Delete old collection if exists
try:
    client.delete_collection(COLLECTION_NAME)
except:
    pass


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def chunk_text(text, chunk_size=1200):

    sentences = sent_tokenize(text)

    chunks = []

    current_chunk = ""

    for sentence in sentences:

        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += " " + sentence

        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def ingest_pdfs():

    total_chunks = 0

    for filename in os.listdir(PDF_DIR):

        if not filename.endswith(".pdf"):
            continue

        pdf_path = os.path.join(PDF_DIR, filename)

        print(f"\nProcessing: {filename}")

        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc):

            text = page.get_text()

            if not text.strip():
                continue

            chunks = chunk_text(text)

            for chunk_idx, chunk in enumerate(chunks):

                embedding = embedding_model.encode(chunk).tolist()

                collection.add(
                    ids=[f"{filename}_{page_num}_{chunk_idx}"],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[
                        {
                            "source": filename,
                            "page": page_num + 1,
                        }
                    ],
                )

                total_chunks += 1

    print(f"\nIndexed {total_chunks} chunks successfully.")


if __name__ == "__main__":
    ingest_pdfs()