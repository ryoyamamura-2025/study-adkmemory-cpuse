import json
from google.genai import types

from ..services import gemini_service as gem

def understand_context(user_input: str) -> str:
    """
    入力文から文脈理解をする関数
   
    Args:
        user_input: ユーザーの入力文
       
    Returns:
        str: 理解した文脈
    """
    context = "ソフトウェアエンジニアで技術的な視点からアドバイスをする"
    return context


def _generate_draft_answer(user_input: str, context: str):
    system_instruction = f'''
以下の情報から応答を作成

ユーザーの入力文: {user_input}
文脈: {context}
'''.format(user_input=user_input, context=context)

    parts = []
    parts.append(types.Part.from_text(text=system_instruction))
    contents=[types.Content(role='user', parts=parts)]
    # print(contents)
    return gem.generate_response(contents)


def generate_draft_answer(user_input: str, context: str) -> str:
    """
    入力文から応答のドラフトを作成する関数
   
    Args:
        user_input: ユーザーの入力文
        context: 理解した文脈
   
    Returns:
        str: 応答のドラフト
    """
    response = _generate_draft_answer(user_input, context)
    return response

