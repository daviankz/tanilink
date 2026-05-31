"""
TaniLink API Server
Handles WhatsApp webhooks and routes to AI Agent.
"""

import os
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import PlainTextResponse
import uvicorn

from agent.core import TaniLinkAgent
from api.whatsapp import send_message, parse_whatsapp_payload

app = FastAPI(
    title="TaniLink API",
    description="AI agent connecting farmers & buyers via WhatsApp",
    version="0.1.0",
)

agent = TaniLinkAgent()
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "tanilink-verify")


@app.get("/webhook")
async def verify_webhook(request: Request):
    """WhatsApp webhook verification."""
    params = dict(request.query_params)
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == WHATSAPP_VERIFY_TOKEN:
        return PlainTextResponse(params.get("hub.challenge"))
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def receive_message(request: Request, background_tasks: BackgroundTasks):
    """Receive incoming WhatsApp messages."""
    payload = await request.json()
    messages = parse_whatsapp_payload(payload)
    for msg in messages:
        background_tasks.add_task(handle_message_task, msg)
    return {"status": "ok"}


async def handle_message_task(msg: dict):
    """Process message and reply via WhatsApp."""
    phone = msg["phone"]
    text = msg["text"]
    role = msg.get("role", "farmer")
    print(f"[TaniLink] {phone} ({role}): {text}")
    reply = agent.handle_message(phone=phone, message=text, role=role)
    send_message(phone=phone, text=reply)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "TaniLink", "version": "0.1.0"}


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
