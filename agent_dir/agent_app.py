import asyncio
import json, os, pprint, time, uuid

from google.genai import types
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import vertexai
from vertexai import agent_engines

from planner_agent.agent import planning_client_agent
from planner_agent.config import APPCONFIG

vertexai.init(
    project=APPCONFIG.GOOGLE_CLOUD_PROJECT,
    location=APPCONFIG.GOOGLE_CLOUD_LOCATION,
    staging_bucket=f"gs://{APPCONFIG.GOOGLE_CLOUD_BUCKET}",
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

# Remoteで推論を実行するためのクラス
class RemoteApp:
    def __init__(self, remote_agent, user_id='default_user'):
        self._remote_agent = remote_agent
        self._user_id = user_id
        self._session = remote_agent.create_session(user_id=self._user_id)
    
    def _stream(self, query, debug=False):
        events = self._remote_agent.stream_query(
            user_id=self._user_id,
            session_id=self._session['id'],
            message=query,
        )
        result = []
        for event in events:
            if debug:
                print(f'----\n{event}\n----')
            if ('content' in event and 'parts' in event['content']):
                response = '\n'.join(
                    [p['text'] for p in event['content']['parts'] if 'text' in p]
                )
                if response:
                    print(response)
                    result.append(response)
        return result

    def stream(self, query, debug=False):
        # Retry 4 times in case of resource exhaustion
        for c in range(4):
            if c > 0:
                time.sleep(2**(c-1))
            result = self._stream(query)
            if result:
                return result
            if debug:
                print('----\nRetrying...\n----')
        return None # Permanent error


def check_resources():
    """Check and list all agent resources."""
    print("Checking agent resources...")

    agents = list(agent_engines.list())

    if not agents:
        print("No agent resources found.")
        return

    print(f"Found {len(agents)} agent(s):")
    for agent in agents:
        print(f"  - {agent.resource_name}")
        # Display available attributes
        try:
            if hasattr(agent, "display_name"):
                print(f"    Display name: {agent.display_name}")
            if hasattr(agent, "create_time"):
                print(f"    Created: {agent.create_time}")
            if hasattr(agent, "update_time"):
                print(f"    Updated: {agent.update_time}")
        except Exception as e:
            print(f"    (Unable to retrieve details: {e})")


# client = LocalApp(planning_client_agent)
agent_engine = agent_engines.get(APPCONFIG.AGENT_RESOURCE_ID)
client = RemoteApp(agent_engine)
# query = "AI開発における2日間の中学生の職場見学会の計画"

def main(query):
    _ = client.stream(query, debug=True)

if __name__ == '__main__':
    check_resources()
    # while True:
    #     user_input = input("input: ")
    #     if user_input == 'exit':
    #         break
    #     main(user_input.strip())
    # #     # asyncio.run(main(user_input.strip()))
