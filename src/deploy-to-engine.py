import sys
from pathlib import Path

import vertexai
from vertexai import agent_engines

from planner_agent.agent import planning_client_agent
from planner_agent.config import APPCONFIG

vertexai.init(
    project=APPCONFIG.GOOGLE_CLOUD_PROJECT,
    location=APPCONFIG.GOOGLE_CLOUD_LOCATION,
    staging_bucket=f"gs://{APPCONFIG.GOOGLE_CLOUD_BUCKET}",
)

remote_planner_agent = agent_engines.create(
    agent_engine=planning_client_agent,
    display_name="planning_client_agent",
    description="プランの生成、更新、評価機能を持つ専門家LLMをツールとして使うAgent",
    requirements=[
        'google-adk==1.4.1',
        'google-cloud-aiplatform==1.97.0',
        'google-genai==1.20.0',
        'python-dotenv'
    ],
    extra_packages=[
        "./planner_agent"
    ]
)