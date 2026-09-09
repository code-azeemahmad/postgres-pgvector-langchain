import asyncio
import os

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from app.search import semantic_search

load_dotenv()


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

LLM_MODEL = os.getenv(
    "OLLAMA_LLM_MODEL",
    "qwem2.5-coder:14b",
)


llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
)


def answer_question(question: str):

    documents = semantic_search(
        question,
        k=3,
        tenant_id="tenant_A",
        department="hr",
    )

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    prompt = f"""
You are a company knowledge assistant.

Answer the question using ONLY the provided context.

Context:
{context}

Question:
{question}

If the answer is not present in the context,
say that you do not know.
"""

    response = llm.invoke(prompt)

    return documents, response.content


def main():

    print("\nCompany Knowledge Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() == "exit":
            break

        documents, answer = answer_question(question)

        print("\nRetrieved documents:")

        for index, doc in enumerate(
            documents,
            start=1,
        ):
            print(
                f"\n[{index}] {doc.page_content}"
            )

        print("\nAssistant:")
        print(answer)
        print()



if __name__ == "__main__":
    main()