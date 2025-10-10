import asyncio
from planner_agent.agent import LocalApp, planning_client_agent

client = LocalApp(planning_client_agent)
# query = "AI開発における2日間の中学生の職場見学会の計画"

async def main(query):
    _ = await client.stream(query, debug=True)

if __name__ == '__main__':
    while True:
        user_input = input("input: ")
        if user_input == 'exit':
            break
        asyncio.run(main(user_input.strip()))
