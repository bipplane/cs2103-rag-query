from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from main import rag_chain

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CS2103 Content Query</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            #query { width: 100%; padding: 12px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px; }
            #submit { margin-top: 10px; padding: 12px 24px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; }
            #submit:hover { background: #0056b3; }
            #submit:disabled { background: #ccc; cursor: not-allowed; }
            #response { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 8px; white-space: pre-wrap; }
            .loading { color: #666; font-style: italic; }
        </style>
    </head>
    <body>
        <h1>CS2103 Content Query</h1>
        <input type="text" id="query" placeholder="Ask a question..." onkeypress="if(event.key==='Enter') askQuestion()">
        <button id="submit" onclick="askQuestion()">Ask</button>
        <div id="response"></div>
        <script>
            async function askQuestion() {
                const query = document.getElementById('query').value;
                const responseDiv = document.getElementById('response');
                const submitBtn = document.getElementById('submit');
                
                if (!query.trim()) return;
                
                submitBtn.disabled = true;
                responseDiv.innerHTML = '<span class="loading">Thinking...</span>';
                
                try {
                    const res = await fetch('/query', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query: query})
                    });
                    const data = await res.json();
                    responseDiv.textContent = data.response;
                } catch (err) {
                    responseDiv.textContent = 'Error: ' + err.message;
                }
                submitBtn.disabled = false;
            }
        </script>
    </body>
    </html>
    """

@app.post("/query")
def query_rag(request: QueryRequest):
    response = rag_chain.invoke(request.query)
    if response is None or response.startswith("Unexpected"):
        repsonse = "An error occurred while processing your request."
    return {"response": response}