import os
import json
import logging
from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

# 1. Initialize FastMCP with your server identity
mcp = FastMCP("RoleRadar-Intelligence-Server")

# Configure professional logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

# --- Tool 1: LinkedIn Job Fetcher ---
@mcp.tool()
async def fetch_linkedin(query: str, limit: int = 10) -> str:
    """
    Fetch real-time job listings from LinkedIn.
    Best for global roles, MNCs, and tech startups.
    """
    try:
        logger.info(f"Searching LinkedIn: {query}")
        jobs = fetch_linkedin_jobs(query, rows=limit)
        return json.dumps(jobs if jobs else [], indent=2)
    except Exception as e:
        logger.error(f"LinkedIn Error: {e}")
        return f"Error: {str(e)}"

# --- Tool 2: Naukri Job Fetcher ---
@mcp.tool()
async def fetch_naukri(query: str, limit: int = 10) -> str:
    """
    Fetch real-time job listings from Naukri.com.
    Optimized for roles in India and major Indian tech hubs.
    """
    try:
        logger.info(f"Searching Naukri: {query}")
        jobs = fetch_naukri_jobs(query, rows=limit)
        return json.dumps(jobs if jobs else [], indent=2)
    except Exception as e:
        logger.error(f"Naukri Error: {e}")
        return f"Error: {str(e)}"

# --- Tool 3: Aggregated Market Scan ---
@mcp.tool()
async def global_market_scan(query: str) -> str:
    """
    Combines results from LinkedIn and Naukri for a comprehensive 
    view of the current job market trends.
    """
    try:
        l_jobs = fetch_linkedin_jobs(query, rows=5)
        n_jobs = fetch_naukri_jobs(query, rows=5)
        return json.dumps({"linkedin": l_jobs, "naukri": n_jobs}, indent=2)
    except Exception as e:
        return f"Scan Failed: {str(e)}"

# --- Render-Specific Deployment Block ---
if __name__ == "__main__":
    # Render assigns a dynamic port via environment variables
    port = int(os.environ.get("PORT", 8000))
    
    # SSE (Server-Sent Events) is required for web-based MCP communication.
    # We bind to 0.0.0.0 so the server is reachable from outside the Render network.
    logger.info(f"🚀 RoleRadar Intelligence Server launching on port {port}")
    
    mcp.run(
        transport="sse", 
        host="0.0.0.0", 
        port=port
    )