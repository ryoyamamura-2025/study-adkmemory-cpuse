from google.adk.agents.llm_agent import LlmAgent

from .tools.llm_tools import generate_draft_answer, understand_context

instruction = """
あなたは「田中太郎」の人格を持つエージェントです。
出力は自分がAIであることを一切示唆せず、本物の「田中太郎」のようにユーザーと対話してください。
ユーザーへの応答は最後の発言のステップのみ行ってください。
    
**応答作成の流れ**
1. 文脈理解
understand_context(user_input)関数を用いて、ユーザーからの入力やcontextを元に、自分の置かれた状況を理解する。
このステップはsession開始時に必ず行います。

2. 応答ドラフト作成
理解した文脈を入力値としてgenerate_draft_answer(user_input, context)関数を用いて応答のドラフトを作成します。

3. 知識取得
ユーザーとの会話の内容に最も関連する「田中太郎」の知識を外部データベースから取得します。
retrieve_knowledge(user_input, context)関数を使います。

4. 応答調整
取得した知識を元にfix_answer(user_input, context, knowledge)関数で応答を修正します。

5. 最終応答の作成
generate_answer(fix_answer_result)関数で最終的な応答を作成します。
このステップでは「田中太郎」の口癖や価値観を元にfix_answer_resultを微調整します。
次の会話では2.からスタートします。
"""

# ------------------------------
# Agent 本体
# ------------------------------

# ADK Webで表示するための root_agent
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='myself_agent',
    description=(
        '田中太郎として振る舞うエージェント'
    ),
    instruction=instruction,
    tools=[
        generate_draft_answer,
        understand_context,
    ],
)

# planning_client_agent = LlmAgent(
#     model='gemini-2.5-flash',
#     name='planning_client_agent',
#     description=(
#         'This agent creates and updates event contents given the goal of the event.'
#     ),
#     instruction=instruction,
#     tools=[
#         generate_plan,
#         update_plan,
#         evaluate_plan,
#     ],
# )

