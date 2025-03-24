from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configure CORS to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data models
class Message(BaseModel):
    text: str

class ChatResponse(BaseModel):
    reply: str

# In-memory storage for demo purposes
chat_history = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Chatbot API"}

@app.post("/chat", response_model=ChatResponse)
async def process_chat(message: Message):
    # Store the user message
    chat_history.append({"role": "user", "content": message.text})
    
    # Simple echo response for demonstration
    response = f"You said: {message.text}"
    
    # Store the bot response
    chat_history.append({"role": "bot", "content": response})
    
    return ChatResponse(reply=response)

@app.get("/history")
async def get_history():
    return chat_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)