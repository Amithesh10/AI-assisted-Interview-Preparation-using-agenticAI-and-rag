import streamlit as st
import requests
from pypdf import PdfReader
from docx import Document

# For local testing:
# API_URL = "http://127.0.0.1:8000"

# Deployment backend URL:
API_URL = "https://ai-assisted-interview-preparation-using.onrender.com"

st.set_page_config(
    page_title="AI Interview Preparation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #0D1B2A !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: #0A1520 !important;
}

.block-container {
    padding-top: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
    max-width: 1400px;
}

.hero-header {
    background: linear-gradient(135deg, #0D1B2A 0%, #0F2744 50%, #0D1B2A 100%);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 16px;
    padding: 36px 40px 28px;
    margin-bottom: 28px;
}

.hero-badge {
    display: inline-block;
    background: rgba(59, 130, 246, 0.12);
    border: 1px solid rgba(59, 130, 246, 0.35);
    color: #60A5FA;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #F8FAFC;
    margin: 0 0 8px;
}

.hero-title span {
    color: #60A5FA;
}

.hero-sub {
    color: #94A3B8;
    font-size: 0.95rem;
    line-height: 1.6;
}

.input-card {
    background: #0F2236;
    border: 1px solid rgba(59, 130, 246, 0.18);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 14px;
}

.input-label {
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #60A5FA;
    margin-bottom: 10px;
    font-weight: 700;
}

.result-card {
    background: #0A1520;
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-left: 4px solid #10B981;
    border-radius: 10px;
    padding: 20px;
    color: #CBD5E1;
    line-height: 1.7;
    margin-top: 16px;
    overflow-x: auto;
}

.stButton > button {
    background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    width: 100%;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

.tab-heading {
    font-size: 1.1rem;
    font-weight: 700;
    color: #F8FAFC;
}

.tab-desc {
    color: #94A3B8;
    margin-bottom: 20px;
}

/* Tablet */
@media (max-width: 1024px) {
    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .hero-header {
        padding: 28px 26px 24px;
    }

    .hero-title {
        font-size: 1.8rem;
    }

    .hero-sub {
        font-size: 0.9rem;
    }

    .input-card {
        padding: 16px;
    }

    [data-testid="stTabs"] [data-baseweb="tab"] {
        font-size: 0.78rem !important;
        padding: 8px 10px !important;
    }
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }

    .hero-header {
        padding: 24px 18px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    .hero-badge {
        font-size: 0.62rem;
        padding: 4px 10px;
        letter-spacing: 0.08em;
    }

    .hero-title {
        font-size: 1.55rem;
        line-height: 1.25;
    }

    .hero-sub {
        font-size: 0.82rem;
        line-height: 1.6;
    }

    .input-card {
        padding: 14px;
        border-radius: 10px;
    }

    .input-label {
        font-size: 0.68rem;
    }

    .stTextArea textarea {
        font-size: 0.82rem !important;
    }

    .stButton > button {
        font-size: 0.82rem !important;
        padding: 9px 14px !important;
    }

    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
    }

    [data-testid="stTabs"] [data-baseweb="tab"] {
        min-width: max-content !important;
        font-size: 0.74rem !important;
        padding: 8px 10px !important;
    }

    .tab-heading {
        font-size: 0.95rem;
    }

    .tab-desc {
        font-size: 0.78rem;
    }

    .result-card {
        padding: 14px;
        font-size: 0.82rem;
    }
}

/* Small Mobile */
@media (max-width: 480px) {
    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .hero-title {
        font-size: 1.35rem;
    }

    .hero-sub {
        font-size: 0.78rem;
    }

    .hero-header {
        padding: 20px 14px;
    }

    .input-card {
        padding: 12px;
    }

    .result-card {
        font-size: 0.78rem;
        line-height: 1.6;
    }
}
</style>
""", unsafe_allow_html=True)


if "outputs" not in st.session_state:
    st.session_state.outputs = {}

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()

    try:
        if name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8", errors="ignore")

        if name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            return "\n".join(page.extract_text() or "" for page in reader.pages)

        if name.endswith(".docx"):
            doc = Document(uploaded_file)
            return "\n".join(p.text for p in doc.paragraphs)

    except Exception as e:
        st.error("File reading failed.")
        st.code(str(e))
        return ""

    return ""


def safe_post(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            st.error(f"Backend error: {response.status_code}")
            st.code(response.text)
            return None

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Backend returned non-JSON response.")
            st.code(response.text)
            return None

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Make sure FastAPI backend is running.")
        st.code(f"Current API_URL = {API_URL}")
        return None

    except requests.exceptions.Timeout:
        st.error("Backend request timed out. Try again.")
        return None

    except Exception as e:
        st.error("Unexpected frontend error.")
        st.code(str(e))
        return None


def run_agent(agent_name, resume, job_desc, company_info, knowledge_text):
    payload = {
        "agent": agent_name,
        "resume": resume,
        "job_desc": job_desc,
        "company_info": company_info,
        "knowledge_text": knowledge_text,
    }

    data = safe_post("/run-agent", payload)

    if not data:
        return None

    if "result" not in data:
        st.error("Backend did not return 'result'.")
        st.code(str(data))
        return None

    return data["result"]


def check_inputs(resume, job_desc):
    if not resume.strip() or not job_desc.strip():
        st.warning("Please enter both resume and job description.")
        return False
    return True


with st.sidebar:
    st.markdown("### ⚡ Knowledge Base")

    kb_option = st.radio(
        "Choose input type",
        ["Type text", "Upload file"]
    )

    knowledge_text = ""

    if kb_option == "Type text":
        knowledge_text = st.text_area(
            "Company notes / interview questions",
            height=220,
            placeholder="Paste company info, interview focus areas, or preparation notes..."
        )
    else:
        uploaded_kb = st.file_uploader(
            "Upload knowledge file",
            type=["txt", "pdf", "docx"]
        )

        if uploaded_kb:
            knowledge_text = extract_text_from_file(uploaded_kb)
            st.success("Knowledge base file loaded")

    st.markdown("---")

    completed = len(st.session_state.outputs)
    total = 5

    st.write(f"Sections completed: **{completed}/{total}**")
    st.progress(completed / total)

    if st.button("Clear Session"):
        st.session_state.outputs = {}
        st.session_state.chat_messages = []
        st.rerun()


st.markdown("""
<div class="hero-header">
    <div class="hero-badge">Agentic AI · RAG · Multi-Agent</div>
    <h1 class="hero-title">AI <span>Interview</span> Preparation</h1>
    <p class="hero-sub">
        Analyze your resume, find skill gaps, generate targeted questions,
        and run a mock interview using AI agents.
    </p>
</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-card"><div class="input-label">Resume</div>', unsafe_allow_html=True)

    resume_mode = st.radio(
        "Resume input mode",
        ["Type text", "Upload file"],
        key="resume_mode",
        horizontal=True
    )

    if resume_mode == "Type text":
        resume = st.text_area(
            "Paste Resume",
            height=220,
            placeholder="Paste your resume here..."
        )
    else:
        uploaded_resume = st.file_uploader(
            "Upload Resume",
            type=["txt", "pdf", "docx"],
            key="resume_upload"
        )
        resume = extract_text_from_file(uploaded_resume) if uploaded_resume else ""

        if uploaded_resume:
            st.success("Resume loaded")

    st.markdown("</div>", unsafe_allow_html=True)


with col2:
    st.markdown('<div class="input-card"><div class="input-label">Job Description</div>', unsafe_allow_html=True)

    jd_mode = st.radio(
        "Job description input mode",
        ["Type text", "Upload file"],
        key="jd_mode",
        horizontal=True
    )

    if jd_mode == "Type text":
        job_desc = st.text_area(
            "Paste Job Description",
            height=220,
            placeholder="Paste job description here..."
        )
    else:
        uploaded_jd = st.file_uploader(
            "Upload Job Description",
            type=["txt", "pdf", "docx"],
            key="jd_upload"
        )
        job_desc = extract_text_from_file(uploaded_jd) if uploaded_jd else ""

        if uploaded_jd:
            st.success("Job description loaded")

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="input-card"><div class="input-label">Company Information</div>', unsafe_allow_html=True)

company_mode = st.radio(
    "Company information input mode",
    ["Type text", "Upload file"],
    key="company_mode",
    horizontal=True
)

if company_mode == "Type text":
    company_info = st.text_area(
        "Company Information",
        height=100,
        placeholder="Paste company details here..."
    )
else:
    uploaded_company = st.file_uploader(
        "Upload Company Info",
        type=["txt", "pdf", "docx"],
        key="company_upload"
    )
    company_info = extract_text_from_file(uploaded_company) if uploaded_company else ""

    if uploaded_company:
        st.success("Company information loaded")

st.markdown("</div>", unsafe_allow_html=True)


tabs = st.tabs([
    "📄 Resume Analyzer",
    "📊 Skill Gap",
    "🧠 Technical Questions",
    "💬 HR Questions",
    "🎤 Mock Interview",
    "📑 Final Report"
])


with tabs[0]:
    st.markdown('<div class="tab-heading">📄 Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-desc">Analyze resume alignment with the job description.</div>', unsafe_allow_html=True)

    if st.button("Analyze Resume", key="btn_resume"):
        if check_inputs(resume, job_desc):
            with st.spinner("Analyzing resume..."):
                result = run_agent("resume", resume, job_desc, company_info, knowledge_text)

                if result:
                    st.session_state.outputs["resume"] = result

    if "resume" in st.session_state.outputs:
        st.markdown(
            f'<div class="result-card">{st.session_state.outputs["resume"]}</div>',
            unsafe_allow_html=True
        )


with tabs[1]:
    st.markdown('<div class="tab-heading">📊 Skill Gap Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-desc">Find missing skills and preparation priorities.</div>', unsafe_allow_html=True)

    if st.button("Analyze Skill Gaps", key="btn_skill"):
        if check_inputs(resume, job_desc):
            with st.spinner("Finding skill gaps..."):
                result = run_agent("skill_gap", resume, job_desc, company_info, knowledge_text)

                if result:
                    st.session_state.outputs["skill_gap"] = result

    if "skill_gap" in st.session_state.outputs:
        st.markdown(
            f'<div class="result-card">{st.session_state.outputs["skill_gap"]}</div>',
            unsafe_allow_html=True
        )


with tabs[2]:
    st.markdown('<div class="tab-heading">🧠 Technical Interview Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-desc">Generate role-specific technical interview questions.</div>', unsafe_allow_html=True)

    if st.button("Generate Technical Questions", key="btn_tech"):
        if check_inputs(resume, job_desc):
            with st.spinner("Generating technical questions..."):
                result = run_agent("technical", resume, job_desc, company_info, knowledge_text)

                if result:
                    st.session_state.outputs["technical"] = result

    if "technical" in st.session_state.outputs:
        st.markdown(
            f'<div class="result-card">{st.session_state.outputs["technical"]}</div>',
            unsafe_allow_html=True
        )


with tabs[3]:
    st.markdown('<div class="tab-heading">💬 HR Interview Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-desc">Generate HR and behavioral interview questions.</div>', unsafe_allow_html=True)

    if st.button("Generate HR Questions", key="btn_hr"):
        if check_inputs(resume, job_desc):
            with st.spinner("Generating HR questions..."):
                result = run_agent("hr", resume, job_desc, company_info, knowledge_text)

                if result:
                    st.session_state.outputs["hr"] = result

    if "hr" in st.session_state.outputs:
        st.markdown(
            f'<div class="result-card">{st.session_state.outputs["hr"]}</div>',
            unsafe_allow_html=True
        )


with tabs[4]:
    st.markdown('<div class="tab-heading">🎤 Mock Interview</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-desc">Chat with an AI interviewer.</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_message = st.chat_input("Type your answer...")

    if user_message:
        if check_inputs(resume, job_desc):
            st.session_state.chat_messages.append(
                {"role": "user", "content": user_message}
            )

            payload = {
                "resume": resume,
                "job_desc": job_desc,
                "company_info": company_info,
                "knowledge_text": knowledge_text,
                "messages": st.session_state.chat_messages,
            }

            with st.spinner("Interviewer is thinking..."):
                data = safe_post("/mock-chat", payload)

            if data and "reply" in data:
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": data["reply"]}
                )
                st.rerun()


with tabs[5]:
    st.markdown('<div class="tab-heading">📑 Final Preparation Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-desc">Generate a complete interview preparation report.</div>', unsafe_allow_html=True)

    if st.button("Generate Final Report", key="btn_report"):
        if check_inputs(resume, job_desc):
            payload = {
                "resume": resume,
                "job_desc": job_desc,
                "company_info": company_info,
                "knowledge_text": knowledge_text,
                "outputs": st.session_state.outputs,
            }

            with st.spinner("Generating report..."):
                data = safe_post("/generate-report", payload)

            if data and "report" in data:
                st.session_state.outputs["report"] = data["report"]

    if "report" in st.session_state.outputs:
        st.markdown(
            f'<div class="result-card">{st.session_state.outputs["report"]}</div>',
            unsafe_allow_html=True
        )
