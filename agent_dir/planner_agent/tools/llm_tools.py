import json
from google.genai import types

from ..services import gemini_service as gem

# 企画生成
def _generate_plan(goal):
    system_instruction = '''
You are a professional event planner. Work on the following tasks.

[task]
A. generate event contents to achieve the given [goal].

[format instruction]
In Japanese. No markdowns. The output has the following three items:
"title": a short title of the event
"summary": three sentence summary of the event
"timeline": timeline of the event such as durations and contents in a bullet list
'''

    response_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "timeline":  {"type": "string"},
        },
        "required": ["title", "summary", "timeline"],
    }

    parts = []
    parts.append(types.Part.from_text(text=f'[goal]\n{goal}'))
    contents=[types.Content(role='user', parts=parts)]
    return gem.generate_response(system_instruction, contents, response_schema)


def generate_plan(goal:str) -> dict:
    """
    Create an initial plan to achieve the goal.
   
    Args:
        goal: The goal of the event.
       
    Returns:
        dict: A dictionary containing the plan with the following keys:
            title: title of the event
            summary: a short summary of the event
            timeline: timeline of the event
    """
    response = _generate_plan(goal)
    return json.loads(response)


# 企画修正
def _update_plan(goal, plan, evaluation):
    system_instruction = '''
You are a professional event planner. Work on the following tasks.

[task]
A. given [goal] and current [plan] for event contents.
   Generate an improved plan based on the given [evaluation].

[format instruction]
In Japanese. No markdowns. The output has the following three items:
"title": a short title of the event
"summary": three sentence summary of the event
"timeline": timeline of the event such as durations and contents in a bullet list
"update: one sentence summary of the update from the previous plan
'''

    response_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "timeline":  {"type": "string"},
            "update": {"type": "string"},
        },
        "required": ["title", "summary", "timeline", "update"],
    }

    parts = []
    parts.append(types.Part.from_text(text=f'[goal]\n{goal}'))
    parts.append(types.Part.from_text(text=f'[plan]\n{plan}'))
    parts.append(types.Part.from_text(text=f'[evaluation]\n{evaluation}'))
    contents=[types.Content(role='user', parts=parts)]
    # print(contents)
    return gem.generate_response(system_instruction, contents, response_schema)


def update_plan(goal:str, plan:str, evaluation:str) -> dict:
    """
    Create an updated plan to achieve the goal given the current plan and an evaluation comment.

    Args:
        goal: The goal of the event
        plan: Current plan
        evaluation: Evaluation comment in plain text or a JSON string
       
    Returns:
        dict: A dictionary containing the plan with the following keys:
            title: title of the event
            summary: a short summary of the event
            timeline: timeline of the event
            update: one sentence summary of the update from the previous plan
    """
    response = _update_plan(goal, plan, evaluation)
    return json.loads(response)

# 企画評価
def _evaluate_plan(goal, plan):
    system_instruction = '''
You are a professional event planner. Work on the following tasks.

[task]
A. given [goal] and [plan] for event contents, evaluate if the plan is effective to achieve the goal.
B. Also give 3 ideas to improve the plan.

[condition]
A. Event contents should include detailed descriptions.

[format instruction]
In Japanese. No markdowns. The output has the following three items:
"evaluation": three sentence evaluation of the plan.
"improvements": a list of 3 ideas to improve the plan. Each idea is in a single sentence.
'''

    response_schema = {
        "type": "object",
        "properties": {
            "evaluation": {"type": "string"},
            "improvements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "idea": {"type": "string"},
                    },
                    "required": ["idea"],
                },
            },
        },
        "required": ["evaluation", "improvements"],
    }

    parts = []
    parts.append(types.Part.from_text(text=f'[goal]\n{goal}'))
    parts.append(types.Part.from_text(text=f'[plan]\n{plan}'))
    contents=[types.Content(role='user', parts=parts)]
    return gem.generate_response(system_instruction, contents, response_schema)


def evaluate_plan(goal:str, plan:str) -> dict:
    """
    Generate an evaluation for the plan against the goal.

    Args:
        goal: The goal of the event
        plan: Current plan
       
    Returns:
        dict: A dictionary containing the evaluation comment with the following keys:
            evaluation: evaluation comment
            improvements: list of ideas for improvements
    """
    response = _evaluate_plan(goal, plan)
    return json.loads(response)
