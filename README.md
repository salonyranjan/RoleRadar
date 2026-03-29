**RoleRadar** is a distributed AI system that bridges the gap between static resumes and the 2026 job market. Built with **Gemini 2.5 Flash** and the **Model Context Protocol (MCP)**, it provides real-time market gap analysis and an automated 6-month career roadmap.

🚀 **[Live Dashboard](https://roleradarz.streamlit.app/)** | 🧠 **[Intelligence Server](https://roleradar-8753.onrender.com/sse)**

---
## 🏗️ Project Architecture

```text
RoleRadar/
├── app.py              # Streamlit Frontend & Session State Management
├── mcp_server.py       # FastMCP Server (Exposes job-fetching tools to LLMs)
├── src/
│   ├── job_api.py      # Backend scrapers for LinkedIn & Naukri (Apify)
│   ├── helper.py       # AI Prompt logic & PDF Extraction utilities
├── .env                # Environment Variables (Ignored by Git)
└── requirements.txt    # Project Dependencies
```

## 🏗️ System Architecture
Unlike traditional monolithic apps, RoleRadar uses a **decoupled, agentic architecture**:

1.  **Frontend (Streamlit Cloud):** A modern, reactive UI for resume parsing and roadmap visualization.
2.  **Intelligence Server (Render):** A high-performance Python backend using **FastMCP**. It hosts custom "tools" that allow Gemini to interact with the real world.
3.  **Agentic Layer (Gemini 2.5):** The "Brain" that orchestrates tool calls to scan LinkedIn and Naukri in real-time based on the user's specific skill set.

---

## ✨ Key Features
* **Context-Aware Analysis:** Extracts deep technical context from PDF resumes.
* **Live Market Scan:** Uses MCP tools to fetch real-time job listings from **LinkedIn** and **Naukri.com**.
* **Strategic Gap Analysis:** Identifies exactly which 2026 skills you are missing for your target roles.
* **Automated Roadmap:** Generates a week-by-week learning plan powered by Gemini.
* **Professional PDF Export:** Download your personalized career strategy report instantly.

---

## 🛠️ Tech Stack
* **LLM:** Google Gemini 2.5 Flash (via Google GenAI SDK)
* **Protocol:** Model Context Protocol (MCP) v2.0
* **Backend:** Python 3.11, FastMCP, Uvicorn (Hosted on Render)
* **Frontend:** Streamlit (Hosted on Community Cloud)
* **APIs:** Apify (Job Scraping), PyMuPDF (Resume Parsing)
* **Reporting:** ReportLab (PDF Generation)
---

## 🚀 Getting Started

### 1. Intelligence Server (Backend)
```bash
cd backend
pip install -r requirements.txt
python mcp_server.py
```
### 2. Frontend (Dashboard)
```bash
pip install -r requirements.txt
streamlit run app.py
```
## 🔑 Environment Variables
Required in both .env (local) and Cloud Secrets (Production):

**GOOGLE_API_KEY: Your Gemini API Key.**

**APIFY_API_TOKEN: To power the job search tools.**

**MCP_SERVER_URL: The URL of your live Render backend.**

---
## 🛠️ Installation & Setup

### 1. Prerequisites
Before you begin, ensure you have the following installed:
* **Python 3.10+** (Miniconda or venv recommended)
* **Node.js & npm** (Required for the MCP Inspector tool)
* **API Keys**: 
    * [Google Gemini API Key](https://ai.google.dev/)
    * [Apify API Key](https://apify.com/) (For LinkedIn/Naukri scraping)

### 2. Clone the Repository
Open your terminal and run:
```bash
git clone [https://github.com/salonyranjan/RoleRadar.git](https://github.com/salonyranjan/RoleRadar.git)
cd RoleRadar
```
### 3. Set Up Environment Variables 🔑

RoleRadar requires access to **Gemini 2.5** for intelligence and **Apify** for live job scraping. 

1. Create a file named `.env` in the root directory of the project.
2. Add the following lines to the file:

```text
# Google Gemini API Key (Get one at: [https://aistudio.google.com/](https://aistudio.google.com/))
GEMINI_API_KEY=your_gemini_api_key_here

# Apify API Key (Get one at: [https://apify.com/](https://apify.com/))
APIFY_API_KEY=your_apify_api_key_here
```
### 4. Install Dependencies 🛠️

It is highly recommended to use a virtual environment (Conda or venv) to manage your RoleRadar dependencies and avoid version conflicts.

**Using Conda (Recommended for Miniconda/Anaconda):**
```bash
# Create a new environment named 'roleradar'
conda create -n roleradar python=3.10 -y

# Activate the environment
conda activate roleradar

# Install all required packages
pip install -r requirements.txt
```
**Using standard Python venv:**
```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```
## 🚦 Running the Application

To experience the full **RoleRadar** workflow, you must launch both the Intelligence Server and the Dashboard simultaneously in separate terminal windows.

### Step 1: Start the MCP Intelligence Server 🧠
In your first terminal, launch the FastMCP server. This provides the AI with "eyes and ears" to fetch live job data from LinkedIn and Naukri.

```bash
# Ensure your virtual environment is active
python mcp_server.py
```
### Step 2: Launch the UI Dashboard 📡
In a second terminal, start the Streamlit frontend. This handles the resume uploads, AI analysis, and PDF generation.

```bash
# Ensure your virtual environment is active
streamlit run app.py
```
---

## 🔍 Testing & Debugging

Before launching the full UI, it is recommended to verify that your **MCP Tools** (LinkedIn & Naukri scrapers) are communicating correctly with the Gemini model.

### 1. Using the MCP Inspector 🛠️
The MCP Inspector provides a web-based interface to manually trigger your tools and see the raw JSON output from the APIs.

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "."; npx @modelcontextprotocol/inspector python mcp_server.py
```
Linux/Mac:

```bash
PYTHONPATH=. npx @modelcontextprotocol/inspector python mcp_server.py
```
---

## 🔍 How to Test: Step-by-Step Verification

To ensure the **RoleRadar** intelligence engine is running correctly, follow these verification steps.

### 1. Verify the Environment 🧪
Before testing, ensure your API keys are loaded and dependencies are installed:
```powershell
# Check if the required libraries are visible
pip show fastmcp apify-client google-generativeai
```
### 2. Test the MCP Intelligence Server (Standalone) 🧠
The MCP Inspector is the professional way to debug AI tools. It creates a local web interface to manually trigger your job-fetching logic.

Run the Inspector Command:

Windows (PowerShell):

```powershell
$env:PYTHONPATH = "."; npx @modelcontextprotocol/inspector python mcp_server.py
```
Linux/Mac:

```bash
PYTHONPATH=. npx @modelcontextprotocol/inspector python mcp_server.py
```
### Verification Steps:

Open your browser to http://localhost:5173.

Click on the "Tools" tab.

You should see fetch_linkedin and fetch_naukri listed.

Click "Run Tool" and enter a JSON query: {"query": "Backend Developer Patna"}.

Success: If you see a JSON list of jobs, your server is officially live!

### 3. End-to-End Dashboard Test 📡
Once the server is verified, test the full integration:

Open a new terminal and run: streamlit run app.py.

Upload a sample Resume (PDF).

Observe the "📡 Initializing Radar Scan..." status.

Success: If the 6-Month Roadmap and Skill Gaps appear, the Gemini 2.5 model has successfully parsed your resume and generated insights.

---

## 🛠️ Common Troubleshooting

If you encounter issues while setting up or running **RoleRadar**, refer to the solutions below for the most common 2026 AI stack challenges.

### 🧩 System & Environment
| Issue | Potential Cause | Solution |
| :--- | :--- | :--- |
| **`mcp` or `npx` not recognized** | Node.js or MCP CLI not in PATH | Install [Node.js](https://nodejs.org/) and run `npm install -m mcp[cli]`. |
| **`ModuleNotFoundError`** | Missing dependencies | Run `pip install -r requirements.txt` in your active environment. |
| **`PYTHONPATH` Errors** | Script can't find `src/` | Ensure you run the Inspector with `$env:PYTHONPATH = "."` (Windows). |

### 🔑 API & Connectivity
| Issue | Potential Cause | Solution |
| :--- | :--- | :--- |
| **`401 Unauthorized`** | Invalid API Keys | Verify your keys in the `.env` file match your [Gemini](https://aistudio.google.dev/) and [Apify](https://apify.com/) consoles. |
| **`429 Rate Limit`** | API Quota exceeded | Wait 60 seconds or upgrade your Gemini tier. The app uses session caching to minimize requests. |
| **Empty Job Results** | Scraper Blocked/Empty Query | Check your Apify Actor logs or try a broader search query like "Software Engineer India". |

### 📡 Application Logic
| Issue | Potential Cause | Solution |
| :--- | :--- | :--- |
| **PDF Extraction Failed** | Image-based PDF | Ensure your resume is a text-based PDF. Scanned images require an OCR layer (e.g., `pytesseract`). |
| **Dashboard Resetting** | Session State loss | Do not refresh the page after uploading; use the "🔄 Clear Session" sidebar button to restart. |
| **Port 8501 in use** | Streamlit conflict | Run `streamlit run app.py --server.port 8502` to use an alternate port. |

---

> [!TIP]
> **Still stuck?** Open a [GitHub Issue](https://github.com/salonyranjan/RoleRadar/issues) with a screenshot of your terminal error and I'll help you debug!

