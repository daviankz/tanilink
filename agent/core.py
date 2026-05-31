"""
TaniLink AI Agent Core
Runs on AMD GPU via ROCm (with cloud fallback)
"""

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFacePipeline

from agent.tools import (
    add_produce_listing,
    get_available_produce,
    notify_buyers,
    get_price_suggestion,
)
from agent.prompts import SYSTEM_PROMPT


def load_local_model(model_id: str = "Qwen/Qwen2.5-7B-Instruct"):
    """Load LLM on AMD GPU via ROCm."""
    print(f"[TaniLink] Loading {model_id} on AMD GPU...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.3,
    )
    return HuggingFacePipeline(pipeline=pipe)


def load_cloud_model():
    """Fallback: cloud LLM when local GPU unavailable."""
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))


def get_llm():
    """Auto-select: local ROCm GPU or cloud fallback."""
    if torch.cuda.is_available():
        try:
            return load_local_model()
        except Exception as e:
            print(f"[TaniLink] Local failed: {e}. Using cloud.")
    return load_cloud_model()


TOOLS = [add_produce_listing, get_available_produce, notify_buyers, get_price_suggestion]


def build_agent():
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True)


class TaniLinkAgent:
    def __init__(self):
        self.agent = build_agent()
        self.sessions: dict[str, list] = {}

    def handle_message(self, phone: str, message: str, role: str = "farmer") -> str:
        history = self.sessions.get(phone, [])
        context = "\n".join([f"{h['role']}: {h['msg']}" for h in history[-5:]])
        enriched_input = (
            f"User role: {role}\n"
            f"Recent conversation:\n{context}\n\n"
            f"Current message: {message}"
        )
        try:
            result = self.agent.invoke({"input": enriched_input})
            reply = result["output"]
        except Exception as e:
            reply = "Maaf, ada gangguan sementara. Silakan coba lagi ya! 🙏"

        self.sessions.setdefault(phone, [])
        self.sessions[phone].append({"role": role, "msg": message})
        self.sessions[phone].append({"role": "agent", "msg": reply})
        return reply
