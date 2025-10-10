import json, os, pprint, time, uuid

from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from tools.llm_tools import generate_plan, update_plan, evaluate_plan

instruction = """
    You are an agent who handles event contents.
    Your outputs should be in Japanese without markdown.
    
    **Interaction flow:**

    1.  Initial plan:
        * When you receive a goal of the event, you should first generate an initial plan using generate_plan().

    2. Present the plan and ask for evaluation:
        * Present the plan to the user, and ask the evaluation and improvement ideas.
            - Show in a human readable format.

    3. (Optional) Get an evaluation from 主任
        * If the user requests to get an evaluation from "主任", get an evaluation using evaluate_plan()
            - Present the result to the user in a human readable format, and ask if the user accept it or not.
        * If the user accept it, go to step 4.
            - When a user say something affirmative, think about if it means to accept 主任's evaluation, or other things.

    4. Upadate plan:
        * Once you get an evaluation from the user or "主任", generate an updated plan using update_plan().
        * Go back to step 2.
"""

# Agent 本体
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='planning_client_agent',
    description=(
        'This agent creates and updates event contents given the goal of the event.'
    ),
    instruction=instruction,
    tools=[
        generate_plan,
        update_plan,
        evaluate_plan,
    ],
)

planning_client_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='planning_client_agent',
    description=(
        'This agent creates and updates event contents given the goal of the event.'
    ),
    instruction=instruction,
    tools=[
        generate_plan,
        update_plan,
        evaluate_plan,
    ],
)

# Localで推論を実行するためのクラス

class LocalApp:
    def __init__(self, agent, user_id='default_user'):
        self._agent = agent
        self._user_id = user_id
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
        self._session = None
        
    async def stream(self, query, debug=False):
        if not self._session:
            self._session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                session_id=uuid.uuid4().hex,
            )
        content = types.Content(role='user', parts=[types.Part.from_text(text=query)])
        async_events = self._runner.run_async(
            user_id=self._user_id,
            session_id=self._session.id,
            new_message=content,
        )
        result = []
        async for event in async_events:
            if debug:
                print(f'----\n{event}\n----')
            if (event.content and event.content.parts):
                response = '\n'.join([p.text for p in event.content.parts if p.text])
                if response:
                    print(response)
                    result.append(response)
        return result

