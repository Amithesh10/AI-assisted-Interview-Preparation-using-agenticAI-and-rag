import streamlit as st
import requests

API_URL = "https://ai-assisted-interview-preparation-using.onrender.com/"

st.set_page_config(
    page_title="AI Interview Prep",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
}

h1 {
    font-size: 32px !important;
    font-weight: 800 !important;
}

h2, h3 {
    font-size: 22px !important;
    font-weight: 700 !important;
}

p, label, div, span {
    font-size: 15px !important;
}

textarea {
    font-size: 14px !important;
}

.stButton button {
    width: 100%;
    height: 44px;
    border-radius: 10px;
    font-size: 15px !important;
    font-weight: 700;
}

.agent-card {
    min-height: 135px;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #3A3F4B;
    background: #171B24;
    color: #F8FAFC;
    box-shadow: 0 3px 12px rgba(0,0,0,0.25);
}

.agent-title {
    font-size: 17px !important;
    font-weight: 800;
    margin-bottom: 8px;
    color: #FFFFFF;
}

.agent-desc {
    font-size: 14px !important;
    color: #CBD5E1;
    line-height: 1.5;
}

.info-box {
    padding: 15px 18px;
    border-radius: 12px;
    background: #172554;
    border: 1px solid #2563EB;
    color: #DBEAFE;
    margin-bottom: 18px;
}

.small-text {
    font-size: 14px !important;
    color: #CBD5E1;
}

.section-title {
    font-size: 22px !important;
    font-weight: 800;
    margin-top: 12px;
    margin-bottom: 16px;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

if "outputs" not in st.session_state:
    st.session_state.outputs = {}

if "mock_messages" not in st.session_state:
    st.session_state.mock_messages = []

if "final_report" not in st.session_state:
    st.session_state.final_report = ""

def safe_api_post(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=180
        )

        if response.status_code != 200:
            return False, f"Backend Error {response.status_code}:\n\n{response.text}"

        return True, response.json()

    except requests.exceptions.ConnectionError:
        return False, "FastAPI backend is not running. Start it using: uvicorn main:app --reload"

    except requests.exceptions.Timeout:
        return False, "Request timed out. Ollama may be slow. Try again."

    except Exception as e:
        return False, f"Error: {str(e)}"

def run_agent(agent_key, resume, job_desc, company_info):
    payload = {
        "agent": agent_key,
        "resume": resume,
        "job_desc": job_desc,
        "company_info": company_info
    }

    success, data = safe_api_post("/run-agent", payload)

    if not success:
        return data

    result = data.get("result", "")

    if not result.strip():
        return "Agent returned blank output."

    return result

st.title("🎯 AI Interview Prep")
st.markdown(
    "<p class='small-text'>Agentic AI + RAG based interview preparation system using Streamlit, FastAPI, Ollama, LangChain, and ChromaDB.</p>",
    unsafe_allow_html=True
)

st.divider()

st.markdown("<div class='section-title'>1. Candidate & Role Details</div>", unsafe_allow_html=True)

left, right = st.columns([1.15, 1])

with left:
    resume = st.text_area(
        "Resume / CV",
        height=240,
        placeholder="Paste your resume text here..."
    )

with right:
    job_desc = st.text_area(
        "Job Description",
        height=155,
        placeholder="Paste job description here..."
    )

    company_info = st.text_area(
        "Company Info Optional",
        height=95,
        placeholder="Company name, domain, culture, role details..."
    )

can_continue = len(resume.strip()) > 50 and len(job_desc.strip()) > 20

if not can_continue:
    st.markdown(
        "<div class='info-box'>Paste your resume and job description to enable the agents.</div>",
        unsafe_allow_html=True
    )

st.divider()

st.markdown("<div class='section-title'>2. Interview Preparation Agents</div>", unsafe_allow_html=True)

agents = {
    "resume": {
        "title": "Resume Agent",
        "desc": "Analyzes resume strengths, skill gaps, ATS score, and improvements."
    },
    "hr": {
        "title": "HR Agent",
        "desc": "Generates HR questions, STAR answers, and communication tips."
    },
    "technical": {
        "title": "Technical Agent",
        "desc": "Creates role-based technical questions, answers, and follow-ups."
    },
    "mock": {
        "title": "Mock Interview",
        "desc": "Conducts a live mock interview with scoring and feedback."
    }
}

cols = st.columns(4)

for index, key in enumerate(agents):
    with cols[index]:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-title">{agents[key]["title"]}</div>
                <div class="agent-desc">{agents[key]["desc"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(f"Run {agents[key]['title']}", disabled=not can_continue, key=f"run_{key}"):

            if key == "mock":
                if len(st.session_state.mock_messages) == 0:
                    payload = {
                        "resume": resume,
                        "job_desc": job_desc,
                        "company_info": company_info,
                        "messages": [
                            {
                                "role": "user",
                                "content": "Start the mock interview. Greet me and ask the first question."
                            }
                        ]
                    }

                    with st.spinner("Starting mock interview..."):
                        success, data = safe_api_post("/mock-chat", payload)

                    if success:
                        reply = data.get("reply", "")
                        if reply.strip():
                            st.session_state.mock_messages.append(
                                {
                                    "role": "assistant",
                                    "content": reply
                                }
                            )
                        else:
                            st.error("Mock interview returned blank output.")
                    else:
                        st.error(data)

                    st.rerun()

            else:
                with st.spinner(f"Running {agents[key]['title']}..."):
                    output = run_agent(
                        key,
                        resume,
                        job_desc,
                        company_info
                    )
                    st.session_state.outputs[key] = output

st.divider()

st.markdown("<div class='section-title'>3. Agent Results</div>", unsafe_allow_html=True)

if len(st.session_state.outputs) == 0:
    st.info("Run an agent to view results here.")

for key, output in st.session_state.outputs.items():
    with st.expander(agents[key]["title"], expanded=True):
        st.markdown(output)

if len(st.session_state.mock_messages) > 0:
    st.divider()

    st.markdown("<div class='section-title'>4. Mock Interview</div>", unsafe_allow_html=True)

    for msg in st.session_state.mock_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_answer = st.chat_input("Type your answer here...")

    if user_answer:
        st.session_state.mock_messages.append(
            {
                "role": "user",
                "content": user_answer
            }
        )

        payload = {
            "resume": resume,
            "job_desc": job_desc,
            "company_info": company_info,
            "messages": st.session_state.mock_messages
        }

        with st.spinner("Evaluating your answer..."):
            success, data = safe_api_post("/mock-chat", payload)

        if success:
            reply = data.get("reply", "")
            st.session_state.mock_messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )
        else:
            st.session_state.mock_messages.append(
                {
                    "role": "assistant",
                    "content": data
                }
            )

        st.rerun()

st.divider()

st.markdown("<div class='section-title'>5. Final Preparation Report</div>", unsafe_allow_html=True)

if st.button("Generate Final Report", disabled=len(st.session_state.outputs) == 0):
    payload = {
        "resume": resume,
        "job_desc": job_desc,
        "company_info": company_info,
        "outputs": st.session_state.outputs
    }

    with st.spinner("Generating final report..."):
        success, data = safe_api_post("/generate-report", payload)

    if success:
        st.session_state.final_report = data.get("report", "")
    else:
        st.session_state.final_report = data

if st.session_state.final_report:
    st.markdown(st.session_state.final_report)
