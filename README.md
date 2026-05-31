# 🌾 TaniLink — AI Agent for Rural Farmers & Buyers

> Connecting farmers to buyers via WhatsApp — powered by LLM inference on AMD ROCm.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![ROCm](https://img.shields.io/badge/AMD-ROCm%206.x-red?logo=amd)](https://rocm.docs.amd.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Business%20API-25D366?logo=whatsapp)](https://developers.facebook.com/docs/whatsapp)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🌍 Problem

Millions of farmers in rural Indonesia lose produce every year simply because they don't know who to sell to. There's no easy way to broadcast availability, match with buyers, or negotiate in real time.

**TaniLink solves this using a WhatsApp AI Agent.**

## 💡 How It Works

```
Farmer (WhatsApp)
      ↓
  "Saya punya 50kg tomat, siap jual hari ini"
      ↓
  TaniLink AI Agent (LLM on AMD ROCm)
  - Parses intent & product data
  - Stores to database
  - Notifies matched buyers
      ↓
  Buyers receive WhatsApp notification
```

## ✨ Features

| Feature | Description |
|---|---|
| 🌾 Farmer Listing | Farmer chats produce availability → auto-stored |
| 🔔 Buyer Notifications | Matched buyers get instant WhatsApp alerts |
| 🤖 Natural Language | Understands Bahasa Indonesia & English |
| 💬 Negotiation Support | Agent facilitates price discussion |
| 💰 Price Insights | Suggests fair market price based on history |
| 🔒 Privacy First | Core inference runs locally on AMD GPU |

## 🏗️ Architecture

```
WhatsApp Users (Farmers & Buyers)
        ↓
  FastAPI Webhook Server
        ↓
  AI Agent (LangChain + Hybrid LLM)
  ├── Primary: AMD GPU via ROCm (Qwen2.5 / Llama3)
  └── Fallback: Cloud LLM API
        ↓
  PostgreSQL Database
```

## 🚀 Quick Start

```bash
git clone https://github.com/daviankz/tanilink.git
cd tanilink
pip install -r requirements.txt
cp .env.example .env
python api/server.py
```

## 🔧 AMD ROCm Integration

```python
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",  # ROCm exposes AMD GPU as 'cuda'
)
```

## 📁 Project Structure

```
tanilink/
├── agent/
│   ├── core.py        # Main AI agent logic
│   ├── tools.py       # DB & notification tools
│   └── prompts.py     # Bilingual system prompts
├── api/
│   ├── server.py      # FastAPI webhook server
│   └── whatsapp.py    # WhatsApp API handler
├── scripts/
│   └── start_model_rocm.sh
├── requirements.txt
└── docker-compose.yml
```

## 🌱 Roadmap

- [x] WhatsApp webhook integration
- [x] Farmer listing via chat
- [x] Buyer notification system
- [ ] Price recommendation engine
- [ ] Voice message support (ASR on ROCm)
- [ ] Multi-language: Javanese, Sundanese

## 📄 License

MIT — Built for the AMD AI Developer Program.
