import os
from dotenv import load_dotenv
from groq import Groq

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import AGENTS
from rag import retrieve_context

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"

app = FastAPI(title="AI Assisted Interview Preparation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentRequest(BaseModel):
    agent: str
    resume: str
    job_desc: str
    company_info: str = ""
    knowledge_text: str = ""


class MockRequest(BaseModel):
    resume: str
    job_desc: str
    company_info: str = ""
    knowledge_text: str = ""
    messages: list


class ReportRequest(BaseModel):
    resume: str
    job_desc: str
    company_info: str = ""
    knowledge_text: str = ""
    outputs: dict


def call_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        if not GROQ_API_KEY:
            return "Groq API key is missing. Please check your .env file."

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=2048,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq API Error: {str(e)}"


def build_query(resume: str, job_desc: str, company_info: str) -> str:
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
        "message": "AI Assisted Interview Preparation Backend is running",
        "api_key_loaded": bool(GROQ_API_KEY),
        "model": MODEL_NAME,
    }


@app.post("/run-agent")
def run_agent(req: AgentRequest):
    try:
        if req.agent not in AGENTS:
            return {"result": "Invalid agent selected."}

        query = build_query(req.resume, req.job_desc, req.company_info)

        rag_context = retrieve_context(
            query=query,
            knowledge_text=req.knowledge_text,
        )

        user_prompt = f"""
Candidate Resume:
{req.resume}

Job Description:
{req.job_desc}

Company Information:
{req.company_info}

Retrieved Knowledge Base Context:
{rag_context}

Selected Agent:
{AGENTS[req.agent]["name"]}

Now perform the selected agent task clearly and professionally.
"""

        result = call_llm(
            AGENTS[req.agent]["system_prompt"],
            user_prompt,
        )

        return {
            "agent": req.agent,
            "result": result,
            "rag_context": rag_context,
        }

    except Exception as e:
        return {
            "agent": req.agent,
            "result": f"Backend error: {str(e)}",
        }


@app.post("/mock-chat")
def mock_chat(req: MockRequest):
    try:
        query = build_query(req.resume, req.job_desc, req.company_info)

        rag_context = retrieve_context(
            query=query,
            knowledge_text=req.knowledge_text,
        )

        conversation = "\n\n".join(
            [
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in req.messages
            ]
        )

        user_prompt = f"""
Candidate Resume:
{req.resume}

Job Description:
{req.job_desc}

Company Information:
{req.company_info}

Retrieved Knowledge Base Context:
{rag_context}

Conversation so far:
{conversation}

Continue the mock interview naturally.
Ask one question at a time.
"""

        reply = call_llm(
            AGENTS["mock"]["system_prompt"],
            user_prompt,
        )

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Backend error: {str(e)}"}


@app.post("/generate-report")
def generate_report(req: ReportRequest):
    try:
        query = build_query(req.resume, req.job_desc, req.company_info)

        rag_context = retrieve_context(
            query=query,
            knowledge_text=req.knowledge_text,
        )

        agent_outputs = "\n\n".join(
            [
                f"=== {key.upper()} ===\n{value}"
                for key, value in req.outputs.items()
            ]
        )

        system_prompt = """
You are a Career Coach and Final Report Agent.
Create a complete interview preparation report.

Use this format:
1. Executive Summary
2. Resume Strengths
3. Skill Gaps
4. Technical Preparation Plan
5. HR Preparation Plan
6. Suggested Interview Questions
7. Readiness Score out of 100
8. Final Motivation
"""

        user_prompt = f"""
Resume:
{req.resume}

Job Description:
{req.job_desc}

Company Information:
{req.company_info}

Retrieved Knowledge Base Context:
{rag_context}

Agent Outputs:
{agent_outputs}

Generate final interview preparation report.
"""

        report = call_llm(system_prompt, user_prompt)

        return {"report": report}

    except Exception as e:
        return {"report": f"Backend error: {str(e)}"}
