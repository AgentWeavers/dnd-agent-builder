from typing import List
from agents import Agent
from pydantic import BaseModel, Field
from planner_agent.subagents.intent_analyzer.intent_prompt import intent_analyzer_agent_prompt_final_v1

class IntentClassification(BaseModel):
    intent: str
    confidence: float

class CompletenessScores(BaseModel):
    technical: float
    functional: float
    requirements: float
    domain: float
    overall: float

class Moscow(BaseModel):
    must: List[str]   
    should: List[str] 
    could: List[str]  
    wont: List[str]   

class DomainSpecific(BaseModel):
    considerations: List[str] 
    best_practices: List[str] 
    challenges: List[str] 

class MissingAspects(BaseModel):
    technical: List[str] 
    functional: List[str] 
    requirements: List[str] 
    domain_specific: DomainSpecific

class IntentOutput(BaseModel):
    purpose_statement: str
    intent_classification: IntentClassification
    refined_query: str
    completeness_scores: CompletenessScores
    moscow: Moscow
    missing_aspects: MissingAspects
    added_requirements: List[str] 
    clarifications_needed:List[str] 
    timestamp: str


intent_analyzer_agent = Agent(
  name="Intent Analyzer",
  model="gpt-4.1-mini",
  instructions=intent_analyzer_agent_prompt_final_v1,
  output_type=IntentOutput
)