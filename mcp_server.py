import os
import json
import logging

# Dual-import strategy for robust version compatibility
try:
    from fastmcp import FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

# 1. Initialize FastMCP with clear identity
# This name helps the LLM understand the tool source
mcp = FastMCP("RoleRadar-Intelligence-Server")

# Configure professional logging for Render Cloud
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_server")

# --- Tool 1: LinkedIn Job Fetcher ---
@mcp.tool()
async def fetch_linkedin(query: str, limit: int = 10) -> str:
    """
    Fetch real-time job listings from LinkedIn.
    Use for global roles, tech startups, and MNCs.
    """
    try:
        logger.info(f"📡 Searching LinkedIn: {query}")
        jobs = fetch_linkedin_jobs(query, rows=limit)
        return json.dumps(jobs if jobs else [], indent=2)
    except Exception as e:
        logger.error(f"❌ LinkedIn Error: {e}")
        return f"Error: {str(e)}"

# --- Tool 2: Naukri Job Fetcher ---
@mcp.tool()
async def fetch_naukri(query: str, limit: int = 10) -> str:
    """
    Fetch real-time job listings from Naukri.com.
    Optimized for Indian tech hubs like Bangalore, Hyderabad, and Pune.
    """
    try:
        logger.info(f"📡 Searching Naukri: {query}")
        jobs = fetch_naukri_jobs(query, rows=limit)
        return json.dumps(jobs if jobs else [], indent=2)
    except Exception as e:
        logger.error(f"❌ Naukri Error: {e}")
        return f"Error: {str(e)}"

# --- Tool 3: Aggregated Market Scan ---
@mcp.tool()
async def global_market_scan(query: str) -> str:
    """
    Performs a combined search across LinkedIn and Naukri.
    Use for a comprehensive overview of the current job market.
    """
    try:
        logger.info(f"📡 Performing Global Scan: {query}")
        l_jobs = fetch_linkedin_jobs(query, rows=5)
        n_jobs = fetch_naukri_jobs(query, rows=5)
        return json.dumps({"linkedin": l_jobs, "naukri": n_jobs}, indent=2)
    except Exception as e:
        logger.error(f"❌ Scan Failed: {e}")
        return f"Scan Failed: {str(e)}"

# --- Render-Specific HTTP Deployment ---
if __name__ == "__main__":
    import os
    # Render's default port is 10000, but we use the environment variable to be safe
    port = int(os.environ.get("PORT", 10000))
    
    logger.info(f"🚀 RoleRadar Intelligence Server: Binding to 0.0.0.0:{port}")
    
    # We MUST use host="0.0.0.0" and transport="http" for Render to see us
    mcp.run(
        transport="http", 
        host="0.0.0.0", 
        port=port
    )