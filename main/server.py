from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from rag import qa_chain  # import your chain from rag.py

app = FastAPI()

# Allow frontend (React) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in dev, open to all; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(req: ChatRequest):
    result = qa_chain({"question": req.question})
    return {
        "answer": result["answer"],
        "sources": [doc.page_content[:200] for doc in result["source_documents"]],
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)