# 🤖 AI Assisted Interview Preparation System

An intelligent interview preparation platform powered by **Agentic AI**, **Retrieval-Augmented Generation (RAG)**, and **Groq LLMs**. The system helps candidates analyze resumes, identify skill gaps, generate interview questions, conduct mock interviews, and receive personalized preparation reports.

---

## 🚀 Features

### 📄 Resume Analyzer Agent

* Analyzes candidate resume against the job description
* Identifies strengths and weaknesses
* Provides resume improvement suggestions
* Highlights matching and missing skills

### 📊 Skill Gap Analyzer Agent

* Compares candidate profile with job requirements
* Detects missing skills
* Generates a personalized learning roadmap
* Creates preparation plans before interviews

### 🧠 Technical Interview Agent

* Generates role-specific technical questions
* Covers:

  * Python
  * Machine Learning
  * Deep Learning
  * Computer Vision
  * SQL
  * FastAPI
  * Generative AI
  * RAG
  * Agentic AI

### 💬 HR Interview Agent

* Generates common HR interview questions
* Provides professional sample answers
* Covers behavioral and situational scenarios

### 🎤 Mock Interview Agent

* Simulates real interview conversations
* Asks questions one at a time
* Evaluates candidate responses

### 📑 Final Report Generator

* Consolidates outputs from all agents
* Generates interview readiness reports
* Provides preparation recommendations

---

## 🏗️ Architecture

```text
User Input
   │
   ▼
Streamlit Frontend
   │
   ▼
FastAPI Backend
   │
   ├── Resume Analyzer Agent
   ├── Skill Gap Agent
   ├── Technical Agent
   ├── HR Agent
   ├── Mock Interview Agent
   │
   ▼
RAG Context Retrieval
   │
   ▼
Groq LLM (Llama 3.3 70B)
   │
   ▼
Generated Insights & Reports
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI
* Python

### LLM

* Groq API
* Llama 3.3 70B Versatile

### AI Concepts

* Agentic AI
* Retrieval-Augmented Generation (RAG)
* Prompt Engineering

### Utilities

* Python-dotenv
* Requests
* PyPDF
* Python-docx

---

## 📂 Project Structure

```text
AI-Interview-Prep
│
├── backend
│   ├── main.py
│   ├── agents.py
│   ├── rag.py
│   ├── requirements.txt
│   └── .env
│
├── frontend
│   ├── app.py
│   └── requirements.txt
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI-Interview-Prep.git
cd AI-Interview-Prep
```

### Backend Setup

```bash
cd backend

python -m venv backendenv

backendenv\Scripts\activate

pip install -r requirements.txt
```

### Create .env File

```env
GROQ_API_KEY=your_groq_api_key
```

### Run Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

---

### Frontend Setup

```bash
cd frontend

pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

Frontend:

```text
http://localhost:8501
```

---

## 📄 Supported Inputs

### Resume

* Text Input
* TXT File
* PDF File
* DOCX File

### Job Description

* Text Input
* TXT File
* PDF File
* DOCX File

### Company Information

* Text Input
* TXT File
* PDF File
* DOCX File

### Knowledge Base

* Custom Notes
* Interview Questions
* Company Information
* Uploaded Documents

---

## 🎯 Use Cases

* AI Engineer Interview Preparation
* Data Scientist Interview Preparation
* Machine Learning Engineer Interviews
* Generative AI Roles
* Data Analyst Roles
* Software Engineer Interviews

---

## 📈 Future Enhancements

* Voice-based mock interviews
* Candidate answer scoring
* ATS Resume Scoring
* Vector Database Integration
* Multi-LLM Support
* Interview Performance Dashboard

---

## 👨‍💻 Author

**Amithesh T S**

Machine Learning | Deep Learning | Computer Vision | Generative AI | Agentic AI

---

## ⭐ If you found this project useful

Give this repository a ⭐ on GitHub.
