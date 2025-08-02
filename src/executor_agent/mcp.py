from agents.mcp import MCPServerSse

def get_context7_mcp_server() -> MCPServerSse:
    """
    Get the Context7 MCP server for OpenAI Agents SDK documentation.
    
    Args:
        None
    
    Returns:
        MCPServerSse: The Context7 MCP server instance.
    """
           
    return MCPServerSse(
        params={
            "url": "https://mcp.context7.com/sse",
        },
        name="Context7 MCP Server",
        cache_tools_list=True
    ) 