import pprint
import tools.llm_tools as llm_tools
import json

goal = "AI開発における2日間の中学生の職場見学会の計画"
plan = llm_tools.generate_plan(goal)
pprint.pp(plan)

evaluation = llm_tools.evaluate_plan(goal, plan)
pprint.pp(evaluation)

plan2 = llm_tools.update_plan(goal, plan, json.dumps(evaluation))
pprint.pp(plan2)