# CS2103/T RAG Query

Uses RAG (and the christmas spirit) to answer questions about CS2103/T course material in the terminal.

<h3 align="center">The aforementioned christmas spirit in question: </h3>
<p align="center">
<img
   src="https://github.com/user-attachments/assets/cbb84596-54fa-4cf5-8564-d2bddd93b02a"
   height = "607"
   object-position: 50% 50%;
   alt="its only funny cuz i made this during christmas season">
</p>


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
# REQUIRED: Google API key (used for embeddings)
GOOGLE_API_KEY=your_google_api_key_here

# OPTIONAL: Add one of these to use a different LLM for queries
# (If not set, Google Gemini will be used for both embeddings and queries)

# OpenAI (for queries)
# OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Claude (for queries)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Note:** 
- **GOOGLE_API_KEY is required** for document embeddings
- Optionally add OPENAI_API_KEY or ANTHROPIC_API_KEY to use their LLMs for answering queries
- Priority for queries: OpenAI → Anthropic → Google (default)

### 3. Ingest the PDF

Run the ingestor **ONCE** to process your PDF and create the vector database:

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
