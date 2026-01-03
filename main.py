import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Google API key REQUIRED for embeddings
if not os.getenv("GOOGLE_API_KEY"):
    print("ERROR: GOOGLE_API_KEY needed for embeddings!")
    print("Please set GOOGLE_API_KEY in your .env file.")
    exit(1)

# Setup embeddings with Google
from langchain_google_genai import GoogleGenerativeAIEmbeddings
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Choose LLM provider (replace model if not working)
if os.getenv("OPENAI_API_KEY"):
    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(model="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY"))
elif os.getenv("ANTHROPIC_API_KEY"):
    from langchain_anthropic import ChatAnthropic
    model = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=os.getenv("ANTHROPIC_API_KEY"))
else:
    from langchain_google_genai import ChatGoogleGenerativeAI
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", api_key=os.getenv("GOOGLE_API_KEY"))

vectorstore = Chroma(persist_directory="./chromadb", embedding_function=embeddings)

# 2. Setup "Retriever" and RAG model
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Get top 3 most relevant chunks

# 4. Create the RAG Chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the following context:
    {context}
    Question: {question}
    Answer:"""
    )

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 5. Loop chat if executing main.py directly (terminal usage)
if __name__ == "__main__":
    while True:
        query = input("\nQuery: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = rag_chain.invoke(query)
        print(f"Bot: {response}")