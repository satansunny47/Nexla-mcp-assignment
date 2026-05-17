import ollama

from app.prompts import SYSTEM_PROMPT


MODEL_NAME = "mistral"


def generate_answer(question, contexts):

    context_text = "\n\n".join(
        [
            f"SOURCE: {c['source']} PAGE: {c['page']}\n{c['content']}"
            for c in contexts
        ]
    )

    prompt = f"""
Question:
{question}

Context:
{context_text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"]