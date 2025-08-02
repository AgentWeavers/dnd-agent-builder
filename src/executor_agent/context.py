import uuid
from typing import Optional, Any, Literal
from enum import Enum
from dataclasses import dataclass, field
from agents import Agent
from src.executor_agent.models import AgentSpecification

class PipelineStage(str, Enum):
    REQUIREMENTS_ANALYSIS = "requirements_analysis"
    CODE_GENERATION = "code_generation"
    CODE_VALIDATION = "code_validation"

STAGES: Literal[PipelineStage.REQUIREMENTS_ANALYSIS, PipelineStage.CODE_GENERATION, PipelineStage.CODE_VALIDATION] = PipelineStage.REQUIREMENTS_ANALYSIS


@dataclass  
class ExecutorContext:  
    """Shared context for executor agent pipeline"""  
      
    # Pipeline State Management  
    current_stage: STAGES = STAGES.REQUIREMENTS_ANALYSIS
    pipeline_id: str = field(default_factory=lambda: str(uuid.uuid4()))  
      
    # Requirements & Specifications  
    raw_requirements: Optional[str] = None  # Original user input  
    parsed_specification: Optional[AgentSpecification] = None  
    validation_results: list[dict[str, Any]] = field(default_factory=list)  
      
    # Generated Artifacts  
    generated_code: dict[str, str] = field(default_factory=dict)  # filename -> code content  
    generated_files: list[str] = field(default_factory=list)  
    project_structure: dict[str, Any] = field(default_factory=dict)  
      
    # Agent Management  
    built_agents: dict[str, Agent] = field(default_factory=dict)  
    active_tools: dict[str, Any] = field(default_factory=dict)  
    mcp_connections: dict[str, Any] = field(default_factory=dict)  
      
    # Execution History & Tracking  
    execution_history: list[dict[str, Any]] = field(default_factory=list)  
    error_log: list[str] = field(default_factory=list)  
    performance_metrics: dict[str, float] = field(default_factory=dict)  
      
    # Session & User Management  
    user_session_id: str = ""  
    workspace_path: str = "./generated_agents"  