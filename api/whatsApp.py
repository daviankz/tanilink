"""
TaniLink WhatsApp Handler
Wraps Meta WhatsApp Business API.
"""

import os
import requests

WHATSAPP_API_URL = "https://graph.facebook.com/v19.0"
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")


def send_message(phone: str, text: str) -> bool:
    """Send a WhatsApp text message."""
    url = f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text},
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    if resp.status_code != 200:
        print(f"[WhatsApp] Failed to send to {phone}: {resp.text}")
        return False
    return True


def parse_whatsapp_payload(payload: dict) -> list[dict]:
    """Extract messages from WhatsApp webhook payload."""
    messages = []
    try:
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                for msg in value.get("messages", []):
                    if msg.get("type") == "text":
                        messages.append({
                            "phone": msg["from"],
                            "text": msg["text"]["body"],
                            "message_id": msg["id"],
                        })
    except Exception as e:
        print(f"[WhatsApp] Parse error: {e}")
    return messages
