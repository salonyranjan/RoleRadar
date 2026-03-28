**RoleRadar** is a next-generation job recommendation engine that moves beyond keyword matching. By leveraging **Generative AI** and the **Model Context Protocol (MCP)**, it provides hyper-personalized career matches by bridging the gap between Large Language Models and real-time data sources.

---

## 🌟 Overview

Traditional job boards often fail because they lack "context"—they can't see your latest projects, your local resume updates, or the nuanced requirements of a job description. 

**RoleRadar** solves this by using **MCP** to securely connect an AI Agent to diverse context servers (GitHub, local files, LinkedIn, etc.), allowing the LLM to "see" your full professional profile before suggesting the perfect role.

## 🚀 Key Features

* **Context-Aware Matching:** Uses MCP to pull real-time data from local resumes and professional portfolios.
* **Semantic Intelligence:** Analyzes the *intent* behind job descriptions rather than just matching keywords.
* **Skill Gap Analysis:** Not only finds jobs but identifies specific skills you need to bridge the gap for a dream role.
* **Agentic Search:** An AI agent that autonomously queries multiple job boards and filters them based on your unique "Professional Context."

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **AI Orchestration:** LangChain / LangGraph
* **Protocol:** Model Context Protocol (MCP) SDK
* **LLM:** Google Gemini 1.5 Pro / Claude 3.5 Sonnet
* **Vector Database:** Pinecone (for semantic search and retrieval)
* **Backend:** FastAPI
* **Frontend:** Streamlit / React

## 🏗️ Architecture

1.  **Context Layer (MCP):** A dedicated MCP server that indexes your local projects, skills, and certifications.
2.  **Reasoning Layer (LLM):** An AI Agent that receives a job query and "calls" the MCP server to fetch your latest relevant experience.
3.  **Matching Engine:** A RAG-based (Retrieval-Augmented Generation) pipeline that scores jobs based on the retrieved context.

