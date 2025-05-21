"""
Lynk.ai Feature Creator - FastAPI Server

This module provides a FastAPI server for the Lynk.ai Feature Creator Agent.
"""
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent import process_input, create_agent



# Create the agent
agent = create_agent()

# Create the FastAPI app
app = FastAPI(
    title="Lynk.ai Feature Creator",
    description="An AI agent that helps users create Lynk.ai feature YAML files.",
    version="0.1.0",
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    session_id: str
    user_id: str = Field(default="TPC-H")


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    user_id: str


# Define the chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and return a response."""
    try:
        # Process the user input
        response = process_input(agent, request.message, request.session_id, user_id=request.user_id, last_message=True)
        
        # Return the response
        return ChatResponse(
            response=response,
            session_id=request.session_id,
            user_id=request.user_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}",
        )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    # Get the port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
