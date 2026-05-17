# Nexla MCP Document QA Server

A local MCP-compatible document question-answering system built for the Nexla Software Engineer take-home assignment.

The system ingests PDF documents, indexes them using semantic embeddings, and exposes a `query_documents` MCP tool that allows AI agents to ask grounded natural-language questions over the document corpus.

---

# Architecture Overview

```text
PDF Documents
    ↓
PyMuPDF Text Extraction
    ↓
Chunking
    ↓
SentenceTransformer Embeddings
    ↓
ChromaDB Vector Store
    ↓
Semantic Retrieval + Reranking
    ↓
Ollama (Mistral)
    ↓
MCP Tool Response
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| MCP Framework | FastMCP |
| PDF Parsing | PyMuPDF |
| Embeddings | sentence-transformers |
| Vector Database | ChromaDB |
| Local LLM | Ollama + Mistral |
| Retrieval Enhancement | CrossEncoder reranking |

---

# Features

- PDF ingestion and indexing
- Semantic search over documents
- MCP-compatible tool interface
- Multi-document retrieval
- Source attribution with page numbers
- Local LLM inference using Ollama
- Retrieval reranking for improved answer quality

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repo_url>
cd nexla-mcp-assignment
```

---

## 2. Create Virtual Environment

```bash
python -m venv myenv
```

Linux/macOS:

```bash
source myenv/bin/activate
```

Windows:

```bash
myenv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Ollama

https://ollama.com

Pull model:

```bash
ollama pull mistral
```

Start Ollama:

```bash
ollama serve
```

---

## 5. Add PDFs

Place PDF files inside:

```text
data/pdfs/
```

---

## 6. Ingest Documents

```bash
python -m app.ingest
```

---

## 7. Start MCP Server

```bash
python -m app.server
```

---

# MCP Tool Documentation

## query_documents

Queries indexed PDF documents using semantic retrieval.

### Input

```json
{
  "question": "What challenges are discussed in the paper?"
}
```

### Output

Grounded answer with source attribution.

Example:

```text
Answer:
 The paper discusses several challenges related to Machine Translation (MT). These challenges include linguistic phenomena such as language-specific idiosyncrasies (SOURCE: P19-1164.pdf PAGE: 5), discourse phenomena (SOURCE: P19-1164.pdf PAGE: 5), pronoun translation (SOURCE: W18-4401.pdf PAGE: 4, SURCE: W18-4401.pdf PAGE: 5), coreference and multiword expressions (SOURCE: W18-4401.pdf PAGE: 5).

Moreover, there is a theoretical gap in the understanding of interrelationships among these challenges, as well as some duplication of research and lack of focus due to the conglomeration of terminologies and understandings of the phenomenon (SOURCE: W18-4401.pdf PAGE: 2). To improve the approach towards solving complex phenomena like this, it is important to achieve a uniform understanding of the problem (SOURCE: W18-4401.pdf PAGE: 2).

```

---

# Example Queries

## Query 1

Question:

```text
What is the primary challenge addressed by the introduction of the Linked WikiText-2 dataset?
```

Answer:

```text
 The primary challenge addressed by the introduction of the Linked WikiText-2 dataset is the need for language models to refer to external sources of information in order to generate factual text, given that each entity mentioned in the dataset is only discussed a few times and is associated with over a thousand different relations (P19-1598.pdf PAGE: 4). The challenge arises due to the complexity of dynamically deciding the facts to incorporate from the knowledge graph, guided by discourse, which traditional language models would not be able to handle effectively.

Reference(s):
- P19-1598.pdf PAGE: 4
```

---

## Query 2

Question:

```text
Which training data size from the Common Crawl resulted in the highest average accuracy across all GLUE tasks?
```

Answer:

```text
 The highest average accuracy across all GLUE tasks was achieved with 18B tokens of Common Crawl data for pretraining, according to the document on page 7 (D19-1539.pdf PAGE: 7).
```

---

# Design Decisions

## Why ChromaDB?

ChromaDB was chosen because it is lightweight, easy to run locally, and suitable for rapid experimentation without external infrastructure dependencies.

## Why Local LLMs?

I chose Ollama with Llama3 to keep the system fully local and reproducible without external API costs or dependencies.

## Why Reranking?

Initial retrieval quality using vector similarity alone was sometimes too broad for research-paper style questions. CrossEncoder reranking improved precision substantially.

---

# Limitations

- No OCR support for scanned PDFs
- No hybrid keyword + semantic retrieval
- No streaming responses
- Retrieval quality depends on chunking strategy

---

# Future Improvements

- Hybrid BM25 + semantic retrieval
- Metadata filtering
- Better citation extraction
- Response streaming
- Support for incremental indexing

---

# Vibe Coding / AI-Assisted Development

I used AI-assisted tooling primarily for:

- brainstorming architecture
- validating MCP integration patterns
- debugging library compatibility issues
- iterating on retrieval pipeline ideas

AI assistance was especially useful for rapidly prototyping boilerplate and exploring different RAG pipeline structures.

However, I manually refined:
- retrieval logic
- chunking strategy
- reranking integration
- project organization
- prompt design

One thing I noticed during development is that AI-generated approaches often overcomplicated the implementation with unnecessary abstractions or frameworks. I intentionally simplified several parts of the system to keep the codebase understandable and maintainable.

Overall, I see AI tooling as a strong productivity multiplier for prototyping and iteration, while engineering judgment remains essential for architecture, tradeoffs, and maintainability.

---

# MCP Validation

The server was tested locally using MCP Inspector over STDIO transport.

---