from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from .prompts import FACILITATOR_INSTRUCTIONS

# 振り分け先
idea_agent = LlmAgent(
    name="IdeaAgent", 
    description="創造的にアイデア出しをする",
    model='gemini-2.5-flash',
    instruction="与えられたトピックに関して誰もがあっと驚くアイデアを1つ出してください。",
)

critic_agent = LlmAgent(
    name="CriticAgent", 
    description="アイデアを評価し批評します。",
    model='gemini-2.5-flash',
    instruction="アイデアに対して建設的な批評を行い改善点を簡潔に提示します。",
)

# 話者の振り分け担当
router_assistant = LlmAgent(
    name="RouterAssistant",
    model="gemini-2.5-flash-lite",
    description="会議参加者に話を振り分けるルーター",
    instruction="ファシリテータからのリクエストのルーティングを行ってください。アイデア出しが必要なときはIdeaAgentに、批評が必要なときはCriticAgentに指示して回答を得た後に回答してください。",
    tools=[agent_tool.AgentTool(agent=idea_agent), agent_tool.AgentTool(agent=critic_agent)]
)

# ファシリ
facilitator_agent = LlmAgent(
    name="Facilitator",
    model="gemini-2.5-flash",
    instruction=FACILITATOR_INSTRUCTIONS,
    tools=[agent_tool.AgentTool(agent=router_assistant)]
    # Alternatively, could use LLM Transfer if research_assistant is a sub_agent
)

root_agent = facilitator_agent