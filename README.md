# CS2103-rag-query

Uses RAG to answer questions about CS2103T course material in the terminal.

## Requirements

- Python 3.10+
- Google API Key

## Setup

### 1. Clone and install dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure .env variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 3. Ingest the PDF

Run the ingestor ONCE to process your PDF and create the vector database:

```bash
python ingestor.py
```

## Usage

Start the chatbot:

```bash
python main.py
```

Then ask questions about your PDF content:

```
Query: What is dependency injection?
Bot: Dependency injection is a technique where...

Query: exit
```

Type `exit` or `quit` to stop the chatbot.