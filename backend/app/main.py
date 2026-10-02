from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.llm import llm_service
from app.services.livekit import livekit_service
from app.agents.registry import registry
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uuid
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-copilot")

app = FastAPI(
    title="AI Copilot Backend",
    description="Agentic AI Assistant with Vision and Voice",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []
    image_base64: Optional[str] = None

class VoiceTokenRequest(BaseModel):
    room: str
    identity: str

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/v1/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        raw_image_base64 = None
        if request.image_base64:
            if "," in request.image_base64:
                raw_image_base64 = request.image_base64.split(",")[1]
            else:
                raw_image_base64 = request.image_base64

        messages = []
        for msg in request.history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        user_message = {"role": "user", "content": request.message}
        if raw_image_base64:
            user_message["images"] = [raw_image_base64]

        messages.append(user_message)

        response_data = await llm_service.generate_chat_response(messages)

        if isinstance(response_data, dict) and response_data.get("type") == "tool_call":
            tool_calls = response_data.get("tool_calls", [])
            tool_results = []

            for call in tool_calls:
                func_name = call.get("function", {}).get("name")
                args = call.get("function", {}).get("arguments", {})

                logger.info(f"Executing skill: {func_name} with args {args}")
                skill = registry.get_skill(func_name)
                if skill:
                    try:
                        result = await skill.run(**args)
                        tool_results.append({"role": "tool", "content": result, "tool_call_id": call.get("id")})
                    except Exception as e:
                        logger.error(f"Skill execution error ({func_name}): {e}")
                        tool_results.append({"role": "tool", "content": f"Error executing skill: {str(e)}", "tool_call_id": call.get("id")})
                else:
                    logger.warning(f"Skill not found: {func_name}")
                    tool_results.append({"role": "tool", "content": "Skill not found", "tool_call_id": call.get("id")})

            final_messages = messages + [{"role": "assistant", "content": "Calling tools..."}] + tool_results
            final_response = await llm_service.generate_chat_response(final_messages)

            if isinstance(final_response, dict):
                return {"response": final_response.get("content", "I processed the tools but couldn't formulate a final answer.")}
            return {"response": final_//response}

        if isinstance(response_data, dict):
            return {"response": response_data.get("content", "I couldn't generate a response.")}

        return {"response": response_data}

    except Exception as e:
        logger.exception("Unexpected error in chat_endpoint")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/voice/token")
async def voice_token_endpoint(request: VoiceTokenRequest):
    try:
        token = await livekit_service.create_token(request.room, request.identity)
        if not token:
            # This will now happen if keys are missing, as requested.
            raise HTTPException(status_code=500, detail="LiveKit API credentials are not configured. Please add them to your .env file.")
        return {"token": token}
    except Exception as e:
        logger.exception("Error generating voice token")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"file_id": file_id, "url": f"/uploads/{file_id}"}
    except Exception as e:
        logger.exception("Error uploading image")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
