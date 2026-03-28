import streamlit as st
import os
import io
import time
from dotenv import load_dotenv

# PDF Generation imports
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT

# RoleRadar Internal Modules
from src.helper import extract_text_from_pdf, get_role_radar_analysis
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

# Load Environment Variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="RoleRadar | AI Job Discovery",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern UI Styling ---
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
        transform: translateY(-3px); 
        border-color: #58a6ff; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .stDownloadButton>button { width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- Professional PDF Generator ---
def generate_pdf_report(analysis):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    
    # Custom style for wrapped text
    custom_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_LEFT
    )
    
    story = []
    story.append(Paragraph("📡 RoleRadar: Career Intelligence Report", styles['Title']))
    story.append(Spacer(1, 20))

    sections = [
        ("📑 Professional Summary", analysis.get('summary', 'N/A')),
        ("🛠️ Strategic Skill Gaps", analysis.get('gaps', 'N/A')),
        ("🚀 6-Month Career Roadmap", analysis.get('roadmap', 'N/A'))
    ]

    for title, text in sections:
        story.append(Paragraph(title, styles['Heading2']))
        # Clean text for PDF compatibility
        clean_text = str(text).replace('\n', '<br/>')
        story.append(Paragraph(clean_text, custom_style))
        story.append(Spacer(1, 15))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --- Sidebar: Control & Branding ---
with st.sidebar:
    st.title("📡 RoleRadar")
    st.status("Model: Gemini 2.5 Flash", state="complete")
    st.info("**Protocol:** MCP v2.0 (Active)")
    st.divider()
    st.markdown("### 👤 Candidate Profile")
    st.caption("Lead Dev: Salony Ranjan")
    st.caption("Environment: 2026 Stable")
    
    if st.button("🔄 Clear Session"):
        st.session_state.clear()
        st.rerun()

# --- Main App Header ---
st.title("📡 Context-Aware Job Discovery")
st.write("Leveraging **Gemini 2.5** to bridge the gap between your resume and the 2026 job market.")

# --- File Upload & Processing Logic ---
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume_uploader")

if uploaded_file:
    # 1. Process PDF and Cache Analysis
    if 'analysis' not in st.session_state:
        with st.status("📡 Initializing Radar Scan...", expanded=True) as status:
            try:
                st.write("Extracting resume context...")
                resume_text = extract_text_from_pdf(uploaded_file)
                
                if not resume_text.strip():
                    st.error("Could not extract text. Please check if the PDF is scanned as an image.")
                    st.stop()

                st.write("Synthesizing Intelligence...")
                analysis_data = get_role_radar_analysis(resume_text)
                
                if "error" in analysis_data:
                    status.update(label="❌ API Rate Limit", state="error")
                    st.error("Gemini is currently throttled. Please try again in 30 seconds.")
                    st.stop()
                
                st.session_state.analysis = analysis_data
                status.update(label="✅ Analysis Synced!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.stop()

    # Reference the analysis
    analysis = st.session_state.analysis

    # 2. Insights Dashboard
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
        
        st.subheader("📄 Export Insights")
        pdf_data = generate_pdf_report(analysis)
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_data,
            file_name=f"RoleRadar_{int(time.time())}.pdf",
            mime="application/pdf"
        )

    # 3. Live Job Search Engine
    st.divider()
    st.header("🔎 Live Market Match")
    
    # Handle keywords (ensure it's a searchable string)
    raw_keywords = analysis.get('keywords', 'Software Engineer')
    query = ", ".join(raw_keywords) if isinstance(raw_keywords, list) else raw_keywords

    if st.button("🚀 Execute Global Job Scan", type="primary"):
        with st.spinner(f"Searching for: {query}..."):
            # Execute fetching (wrapped in try-except for API safety)
            try:
                linkedin_results = fetch_linkedin_jobs(query, rows=10)
                naukri_results = fetch_naukri_jobs(query, rows=10)
                
                st.session_state.linkedin_jobs = linkedin_results
                st.session_state.naukri_jobs = naukri_results
            except Exception as e:
                st.error(f"Search failed: {e}")

    # Display results if they exist in session state
    if 'linkedin_jobs' in st.session_state or 'naukri_jobs' in st.session_state:
        tab_l, tab_n = st.tabs(["LinkedIn Opportunities", "Naukri (India)"])

        with tab_l:
            jobs = st.session_state.get('linkedin_jobs', [])
            if jobs:
                for job in jobs:
                    st.markdown(f"""
                        <div class="job-card" style="border-left: 5px solid #0077b5;">
                            <h4 style="margin:0;">{job.get('title', 'Unknown Title')}</h4>
                            <p style="margin:5px 0; color:#8b949e;">🏢 <b>{job.get('companyName', 'N/A')}</b> | 📍 {job.get('location', 'Remote')}</p>
                            <a href="{job.get('link', '#')}" target="_blank" style="color:#58a6ff; text-decoration:none; font-weight:bold;">Apply on LinkedIn →</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No active LinkedIn matches found for these keywords.")

        with tab_n:
            jobs = st.session_state.get('naukri_jobs', [])
            if jobs:
                for job in jobs:
                    st.markdown(f"""
                        <div class="job-card" style="border-left: 5px solid #4a90e2;">
                            <h4 style="margin:0;">{job.get('title', 'Unknown Title')}</h4>
                            <p style="margin:5px 0; color:#8b949e;">🏢 <b>{job.get('companyName', 'N/A')}</b> | 📍 {job.get('location', 'India')}</p>
                            <a href="{job.get('url', '#')}" target="_blank" style="color:#58a6ff; text-decoration:none; font-weight:bold;">Apply on Naukri →</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No active Naukri matches found.")

else:
    # Landing Page State
    st.markdown("---")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("https://img.icons8.com/fluency/240/radar.png", width=120)
        st.markdown("### Welcome to the Future of Job Hunting")
        st.write("Upload your resume to generate a gap analysis and live job feed.")