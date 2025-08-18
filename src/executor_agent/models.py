from typing import Optional, Any, ForwardRef, Annotated
from pydantic import BaseModel, Field

class ToolSpecification(BaseModel):
    """Structured tool specification returned by Requirement Analysis Agent"""
    name: str = Field(description="The name of the tool")
    tool_type: str = Field(description="The type of tool", default="custom_function")
    file_name: str = Field(description="The implementation file name of the tool", default="tools/tool_name.py")
    description: str = Field(description="A brief description of the tool")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Tool parameters schema")  
    is_enabled: bool = Field(default=True, description="Whether tool is enabled")


class BaseAgentSpecification(BaseModel):
    """Structured agent specification returned by Requirement Analysis Agent"""
    # Agent Metadata
    name: str = Field(description="The name of the agent")
    version: Optional[str] = Field(description="The version of the agent", default="1.0.0")
    description: str = Field(description="A brief description of the agent")
    tags: Optional[list[str]] = Field(description="A list of tags for the agent", default_factory=list)
    
    # Agent Configuration
    model: str = Field(description="The model to use for the agent", default="gpt-4.1-mini")
    temperature: Optional[float] = Field(description="The temperature to use for the agent", default=0.5)
    max_tokens: Optional[int] = Field(description="The maximum number of tokens to use for the agent", default=1000)
    top_p: Optional[float] = Field(description="The top p to use for the agent", default=None)
    tool_choice: Optional[str] = Field(description="The tool choice to use for the agent", default=None)
    instructions: Optional[str] = Field(description="The instructions for the agent")
    
    # Tools
    tools: Optional[list[ToolSpecification]] = Field(description="The tools to use for the agent", default_factory=list)
    
    # Context
    context: Optional[dict[str, Any]] = Field(description="The context for the agent", default=None)

    # MCP Servers
    mcp_servers: Optional[list[dict[str, Any]]] = Field(description="The MCP servers to use for the agent", default_factory=list)

    # Handoffs
    handoffs: Optional[list[str]] = Field(description="The handoffs to use for the agent", default_factory=list)
    
    # Handoff Description
    handoff_description: Optional[str] = Field(description="The handoff description for the agent", default=None)
    
    # Others
    output_type: Optional[str] = Field(None, description="Structured output type class name")  
    output_schema: Optional[dict[str, Any]] = Field(None, description="JSON schema for output")
    
    class Config:  
        extra = "forbid"

class AgentSpecification(BaseAgentSpecification):
    sub_agents: list[Annotated[BaseAgentSpecification, Field(description="List of sub-agents")]] = Field(default_factory=list)
    
    class Config(BaseAgentSpecification.Config):
        pass