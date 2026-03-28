import json
import logging
from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

# 1. Initialize FastMCP with a clear identity
# This name is how the LLM identifies the source of the tools
mcp = FastMCP("JobRadar-Intelligence-Server")

# Configure logging for debugging stdio transport issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

# --- Tool 1: LinkedIn Job Fetcher ---
@mcp.tool()
async def fetch_linkedin(query: str, limit: int = 10) -> str:
    """
    Fetch real-time job listings from LinkedIn.
    Use this for global roles, tech startups, and multinational corporations.
    
    Args:
        query: Search terms (e.g., 'Senior Python Developer Remote')
        limit: Number of results to return (default 10)
    """
    try:
        logger.info(f"Searching LinkedIn for: {query}")
        jobs = fetch_linkedin_jobs(query, rows=limit)
        
        if not jobs:
            return f"No LinkedIn results found for '{query}'."
            
        return json.dumps(jobs, indent=2)
    except Exception as e:
        logger.error(f"LinkedIn Fetch Error: {e}")
        return f"Error accessing LinkedIn API: {str(e)}"

# --- Tool 2: Naukri Job Fetcher ---
@mcp.tool()
async def fetch_naukri(query: str, limit: int = 10) -> str:
    """
    Fetch real-time job listings from Naukri.com.
    Best used for roles specifically located in India or for Indian tech hubs.
    
    Args:
        query: Search terms (e.g., 'Data Scientist Bangalore')
        limit: Number of results to return (default 10)
    """
    try:
        logger.info(f"Searching Naukri for: {query}")
        jobs = fetch_naukri_jobs(query, rows=limit)
        
        if not jobs:
            return f"No Naukri results found for '{query}'."
            
        return json.dumps(jobs, indent=2)
    except Exception as e:
        logger.error(f"Naukri Fetch Error: {e}")
        return f"Error accessing Naukri API: {str(e)}"

# --- Tool 3: Aggregated Market Scan ---
@mcp.tool()
async def global_market_scan(query: str) -> str:
    """
    Performs a combined search across LinkedIn and Naukri.
    Use this when a user wants a comprehensive overview of the current market.
    """
    try:
        l_jobs = fetch_linkedin_jobs(query, rows=5)
        n_jobs = fetch_naukri_jobs(query, rows=5)
        
        combined = {
            "linkedin": l_jobs if l_jobs else [],
            "naukri": n_jobs if n_jobs else []
        }
        return json.dumps(combined, indent=2)
    except Exception as e:
        return f"Market Scan Failed: {str(e)}"

if __name__ == "__main__":
    # transport='stdio' is the standard for MCP, allowing 
    # Claude Desktop, Gemini, or custom clients to pipe commands in/out.
    mcp.run(transport='stdio')