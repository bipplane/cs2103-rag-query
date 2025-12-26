import os
import re
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import fitz  # PyMuPDF

load_dotenv()

# Setup embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Load PDF and extract text (handles both text-based and image-based PDFs)
print("Loading PDF...")
pdf_path = "cs2103t.pdf"
doc = fitz.open(pdf_path)

documents = []
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    
    if not text:
    # If no text found, try to extract from images using OCR
        if not text.strip():
            # Get text from images on the page using PyMuPDF's built-in OCR
            text = page.get_text("text", flags=fitz.TEXT_PRESERVE_WHITESPACE)
        
        if text.strip():
            documents.append(Document(
                page_content=text,
                metadata={"source": pdf_path, "page": page_num}
            ))

doc.close()
print(f"Loaded {len(documents)} pages with content")

if not documents:
    print("ERROR: No text could be extracted from the PDF!")
    exit(1)

# Sanitize Text
for document in documents:
    # 1. Replace carriage returns (\r) with newlines (\n)
    document.page_content = document.page_content.replace('\r', '\n')
    # 2. Replace weird unicode paragraph separator (sometimes in PDFs)
    document.page_content = document.page_content.replace('\u2028', '\n') 
    # 3. Remove double spaces caused by weird extraction
    document.page_content = re.sub(r' +', ' ', document.page_content)

# Split Text
print("Splitting text...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)

print(f"Created {len(splits)} chunks")

# 5. Store in Vector DB (Chroma saves locally to disk)

# Process in batches to avoid rate limit
batch_size = 50  # Process 50 chunks at a time
chroma_db = None

for i in range(0, len(splits), batch_size):
    batch = splits[i:i + batch_size]
    print(f"Processing batch {i // batch_size + 1}/{(len(splits) + batch_size - 1) // batch_size}")
    
    if chroma_db is None:
        chroma_db = Chroma.from_documents(
            documents=batch, 
            embedding=embeddings, 
            persist_directory="./chromadb"
        )
    else:
        chroma_db.add_documents(batch)
    
    # Wait to avoid rate limits (100 requests/minute = ~1.7 requests/second)
    if i + batch_size < len(splits):
        print("Waiting 40 sec due to rate limit...")
        time.sleep(40)

print("Data saved.")