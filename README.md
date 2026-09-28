# ⚡ Autonomous Text-to-SQL LangGraph Agent

An autonomous Agentic AI system built with **LangGraph** and **Groq** that converts natural language business queries into verified SQLite queries, executes them against an e-commerce database, and synthesizes clear answers.

---

## 🏗️ Architecture & Workflow

1. **`sql_generator_node`**: Writes schema-accurate SQLite queries using Groq (`qwen/qwen3.8-27b`).
2. **`query_executor_node`**: Enforces a safe, read-only SQL execution pipeline against `olist.db`.
3. **`response_generator_node`**: Synthesizes clean natural language answers from raw data.

[START] ──► [sql_generator] ──► [query_executor] ──► [response_generator] ──► [END]

---

## 🛠️ Tech Stack

- **Orchestration:** LangGraph (StateGraph)
- **LLM Engine:** Groq API (`qwen/qwen3.8-27b`)
- **Database:** SQLite3 (`olist.db`)
- **Framework:** LangChain Core, Python-dotenv, Pandas

---

## 🚀 Setup & Execution

1. **Clone repo & install dependencies:**
   ```bash
   git clone <your-repo-link>
   cd Shipment-Exception-Investigator
   pip install -r requirements.txt