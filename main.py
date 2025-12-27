import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vectorstore = Chroma(persist_directory="./chromadb", embedding_function=embeddings)

# 2. Setup "Retriever" and RAG model
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Get top 3 most relevant chunks
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", api_key=os.getenv("GOOGLE_API_KEY"))

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

# 5. Loop to chat
while True:
    query = input("\nQuery: ")
    if query.lower() in ["exit", "quit"]:
        break
    response = rag_chain.invoke(query)
    print(f"Bot: {response}")