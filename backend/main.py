from fastapi import FastAPI
from pydantic import BaseModel
import requests
from agents import AGENTS
from rag import retrieve_context

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"

class AgentRequest(BaseModel):
    agent: str
    resume: str
    job_desc: str
    company_info: str = ""

class MockRequest(BaseModel):
    resume: str
    job_desc: str
    company_info: str = ""
    messages: list

class ReportRequest(BaseModel):
    resume: str
    job_desc: str
    company_info: str = ""
    outputs: dict

def call_ollama(system_prompt, messages):
    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            }
        ] + messages
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]

def build_query(resume, job_desc, company_info):
    return f"""
Resume:
{resume}

Job Description:
{job_desc}

Company Information:
{company_info}
"""

@app.get("/")
def home():
    return {
        "message": "Agentic AI + RAG Interview Prep Backend is running"
    }

@app.post("/run-agent")
def run_agent(req: AgentRequest):
    if req.agent not in AGENTS:
        return {
            "result": "Invalid agent selected."
        }

    query = build_query(
        req.resume,
        req.job_desc,
        req.company_info
    )

    rag_context = retrieve_context(query)

    user_prompt = f"""
Candidate Resume:
{req.resume}

Job Description:
{req.job_desc}

Company Information:
{req.company_info}

Retrieved RAG Knowledge:
{rag_context}

Now perform the task for the selected agent.
"""

    result = call_ollama(
        AGENTS[req.agent]["system_prompt"],
        [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return {
        "agent": req.agent,
        "result": result,
        "rag_context": rag_context
    }

@app.post("/mock-chat")
def mock_chat(req: MockRequest):
    query = build_query(
        req.resume,
        req.job_desc,
        req.company_info
    )

    rag_context = retrieve_context(query)

    system_prompt = f"""
{AGENTS["mock"]["system_prompt"]}

Candidate Resume:
{req.resume}

Job Description:
{req.job_desc}

Company Information:
{req.company_info}

Retrieved RAG Knowledge:
{rag_context}
"""

    result = call_ollama(
        system_prompt,
        req.messages
    )

    return {
        "reply": result
    }

@app.post("/generate-report")
def generate_report(req: ReportRequest):
    query = build_query(
        req.resume,
        req.job_desc,
        req.company_info
    )

    rag_context = retrieve_context(query)

    agent_outputs = "\n\n".join(
        [f"=== {key.upper()} ===\n{value}" for key, value in req.outputs.items()]
    )

    system_prompt = """
You are a Career Coach and Final Report Agent.

Create a complete interview preparation report.

Use this format:

1. EXECUTIVE SUMMARY
2. TOP STRENGTHS
3. CRITICAL SKILL GAPS
4. TECHNICAL PREPARATION PLAN
5. HR PREPARATION PLAN
6. TOP 10 INTERVIEW TIPS
7. PREDICTED INTERVIEW READINESS SCORE
8. FINAL MOTIVATION
"""

    user_prompt = f"""
Resume:
{req.resume}

Job Description:
{req.job_desc}

Company Information:
{req.company_info}

Retrieved RAG Knowledge:
{rag_context}

Agent Outputs:
{agent_outputs}

Generate final report.
"""

    result = call_ollama(
        system_prompt,
        [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return {
        "report": result
    }