from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat import generate_response

app = FastAPI()

# Configure CORS for Electron frontend or React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

class ChatResponse(BaseModel):
    reply: str

chat_history = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Chatbot API"}

@app.post("/chat", response_model=ChatResponse)
async def process_chat(message: Message):
    chat_history.append({"role": "user", "content": message.text})

    try:
        response_text = generate_response(message.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    chat_history.append({"role": "bot", "content": response_text})

    return ChatResponse(reply=response_text)

@app.get("/history")
async def get_history():
    return chat_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)