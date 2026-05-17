from fastmcp import FastMCP

from app.retriever import retrieve_context
from app.llm import generate_answer


mcp = FastMCP("Nexla Document QA Server")


@mcp.tool()
def query_documents(question: str) -> str:
    """
    Query the indexed PDF documents.

    Args:
        question: Natural language question

    Returns:
        Grounded answer with source attribution
    """

    contexts = retrieve_context(question)

    answer = generate_answer(question, contexts)

    return answer


if __name__ == "__main__":
    mcp.run(transport="stdio")