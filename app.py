import streamlit as st
import os
import io
import time
import json
import asyncio
from dotenv import load_dotenv

# MCP & SSE Connection Protocol
from mcp import ClientSession
from mcp.client.sse import sse_client

# Professional Reporting
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT

# RoleRadar Internal Core
from src.helper import extract_text_from_pdf, get_role_radar_analysis

# Load Environment Variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="RoleRadar | AI Job Discovery",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Persistence ---
# This ensures data survives browser refreshes and external redirects
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'linkedin_jobs' not in st.session_state:
    st.session_state.linkedin_jobs = []
if 'naukri_jobs' not in st.session_state:
    st.session_state.naukri_jobs = []

# --- Custom UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #c9d1d9; }
    .job-card { 
        background-color: #161b22; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #30363d;
        margin-bottom: 15px;
        transition: transform 0.2s, border-color 0.2s;
    }
    .job-card:hover { 
        transform: translateY(-3.5px); 
        border-color: #58a6ff; 
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #238636; color: white; }
    .stDownloadButton>button { width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- MCP Intelligence Bridge ---
async def fetch_market_data(query):
    """Securely communicates with the Render Intelligence Server."""
    url = st.secrets.get("MCP_SERVER_URL", "https://roleradar-8753.onrender.com/sse")
    try:
        # sse_client handles the 'text/event-stream' handshake automatically
        async with sse_client(url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                # Trigger the 'global_market_scan' tool on your Render server
                result = await session.call_tool("global_market_scan", arguments={"query": query})
                # Parse the tool's content (which returns a JSON string)
                return json.loads(result.content[0].text)
    except Exception as e:
        st.error(f"📡 Intelligence Server Connection Failed: {e}")
        return None

# --- PDF Export Engine ---
def generate_pdf_report(analysis):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, leading=14, alignment=TA_LEFT)
    
    story = [Paragraph("📡 RoleRadar: Career Intelligence Report", styles['Title']), Spacer(1, 20)]
    sections = [
        ("📑 Professional Summary", analysis.get('summary', 'N/A')),
        ("🛠️ Strategic Skill Gaps", analysis.get('gaps', 'N/A')),
        ("🚀 6-Month Career Roadmap", analysis.get('roadmap', 'N/A'))
    ]

    for title, text in sections:
        story.append(Paragraph(title, styles['Heading2']))
        story.append(Paragraph(str(text).replace('\n', '<br/>'), custom_style))
        story.append(Spacer(1, 15))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --- Sidebar: branding & Controls ---
with st.sidebar:
    st.title("📡 RoleRadar")
    st.status("Model: Gemini 2.5 Flash", state="complete")
    st.info("**Protocol:** MCP v2.0 (Active)")
    st.divider()
    st.markdown("### 👤 Candidate Profile")
    st.caption("Lead Dev: Salony Ranjan")
    st.caption("Location: Patna, Bihar")
    
    if st.button("🔄 Clear Analysis & Reset"):
        st.session_state.clear()
        st.rerun()

# --- Main Dashboard ---
st.title("📡 Context-Aware Job Discovery")
st.write("Leveraging **Agentic AI** to sync your resume with the live 2026 job market.")

# --- Upload Logic ---
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume_uploader")

if uploaded_file:
    # 1. AI Analysis Phase
    if st.session_state.analysis is None:
        with st.status("📡 Initializing Radar Scan...", expanded=True) as status:
            try:
                st.write("Extracting resume context...")
                resume_text = extract_text_from_pdf(uploaded_file)
                
                if not resume_text.strip():
                    st.error("Empty PDF. Please check your file.")
                    st.stop()

                st.write("Synthesizing Intelligence with Gemini...")
                analysis_data = get_role_radar_analysis(resume_text)
                
                if "error" in analysis_data:
                    status.update(label="❌ API Rate Limit", state="error")
                    st.error("Gemini is throttled. Waiting 30s...")
                    time.sleep(30)
                    st.rerun()
                
                st.session_state.analysis = analysis_data
                status.update(label="✅ Analysis Synced!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"System Error: {e}")
                st.stop()

    # 2. Results Dashboard
    analysis = st.session_state.analysis
    st.divider()
    col_main, col_stats = st.columns([2, 1], gap="large")

    with col_main:
        st.subheader("📑 Professional Summary")
        st.info(analysis.get('summary', 'No summary generated.'))
        st.subheader("🚀 6-Month Strategic Roadmap")
        st.success(analysis.get('roadmap', 'No roadmap generated.'))

    with col_stats:
        st.subheader("🛠️ Skill Gaps")
        st.warning(analysis.get('gaps', 'No gaps identified.'))
        st.subheader("📄 Export Report")
        pdf_data = generate_pdf_report(analysis)
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_data,
            file_name=f"RoleRadar_Report.pdf",
            mime="application/pdf"
        )

    # 3. Job Search Engine (MCP Interaction)
    st.divider()
    st.header("🔎 Live Market Match")
    
    # Extract search query from AI keywords
    raw_keywords = analysis.get('keywords', 'Software Engineer')
    query = ", ".join(raw_keywords) if isinstance(raw_keywords, list) else raw_keywords

    if st.button("🚀 Execute Global Job Scan", type="primary"):
        with st.spinner(f"🔍 AI is scanning market for: {query}..."):
            market_data = asyncio.run(fetch_market_data(query))
            if market_data:
                st.session_state.linkedin_jobs = market_data.get("linkedin", [])
                st.session_state.naukri_jobs = market_data.get("naukri", [])
                st.success("✅ Market Intelligence Synced!")

    # Display Jobs in Tabs
    if st.session_state.linkedin_jobs or st.session_state.naukri_jobs:
        tab_l, tab_n = st.tabs(["LinkedIn Matches", "Naukri (India)"])

        with tab_l:
            for job in st.session_state.linkedin_jobs:
                st.markdown(f"""
                    <div class="job-card" style="border-left: 5px solid #0077b5;">
                        <h4 style="margin:0;">{job.get('title', 'Role')}</h4>
                        <p style="margin:5px 0; color:#8b949e;">🏢 <b>{job.get('companyName', 'N/A')}</b> | 📍 {job.get('location', 'Remote')}</p>
                        <a href="{job.get('link', '#')}" target="_blank" rel="noopener noreferrer" style="color:#58a6ff; text-decoration:none; font-weight:bold;">Apply on LinkedIn →</a>
                    </div>
                """, unsafe_allow_html=True)

        with tab_n:
            for job in st.session_state.naukri_jobs:
                st.markdown(f"""
                    <div class="job-card" style="border-left: 5px solid #4a90e2;">
                        <h4 style="margin:0;">{job.get('title', 'Role')}</h4>
                        <p style="margin:5px 0; color:#8b949e;">🏢 <b>{job.get('companyName', 'N/A')}</b> | 📍 {job.get('location', 'India')}</p>
                        <a href="{job.get('url', '#')}" target="_blank" rel="noopener noreferrer" style="color:#58a6ff; text-decoration:none; font-weight:bold;">Apply on Naukri →</a>
                    </div>
                """, unsafe_allow_html=True)
else:
    # Landing View
    st.markdown("---")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("https://img.icons8.com/fluency/240/radar.png", width=120)
        st.markdown("### Ready to find your next move?")
        st.write("Upload your resume and let the AI Radar scan the 2026 job market for you.")
