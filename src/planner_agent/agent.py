from google.adk.agents.llm_agent import LlmAgent

from .tools.llm_tools import generate_plan, update_plan, evaluate_plan

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

# ------------------------------
# Agent 本体
# ------------------------------

# ADK Webで表示するための root_agent
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

