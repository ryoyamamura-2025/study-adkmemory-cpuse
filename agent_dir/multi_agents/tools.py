import os
from google import genai
from google.genai import types

from .config import APP_CONFIG

def _generate_response_(prompt, model='gemini-2.5-flash'):
    # Geminiクライアント初期化
    _client = genai.Client(
        vertexai=True,
        project=APP_CONFIG.GOOGLE_CLOUD_PROJECT,
        location=APP_CONFIG.GOOGLE_CLOUD_LOCATION,
    )

    input_prompt = types.Part.from_text(text=prompt.strip())
    contents = [
        types.Content(
            role = "user",
            parts = [
                input_prompt
            ]
        ),
    ]

    response = _client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=65535,
        )
    )

    return response.tex

def _generate_response_with_search(prompt, model='gemini-2.5-flash'):
    # Geminiクライアント初期化
    _client = genai.Client(
        vertexai=True,
        project=APP_CONFIG.GOOGLE_CLOUD_PROJECT,
        location=APP_CONFIG.GOOGLE_CLOUD_LOCATION,
    )

    grounding_tool = types.Tool(google_search=types.GoogleSearch())

    prompt = "「" + prompt.strip() + "」" + "について調査し、結果を報告してください"
    input_prompt = types.Part.from_text(text=prompt.strip())
    contents = [
        types.Content(
            role = "user",
            parts = [
                input_prompt
            ]
        ),
    ]

    response = _client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1000,
            tools=[grounding_tool],
        )
    )

    return response.text


def web_search(search_target: str) -> str:
    """
    調査対象項目を調査して調査内容を生成する

    Args:
        search_target (str): 調査対象の項目

    Returns:
        str: 調査結果のテキスト
    """

    return _generate_response_with_search(search_target)

def summarize(text: str) -> str:
    """
    調査結果を要約する

    Args:
        text (str): 調査結果のテキスト

    Returns:
        str: 要約結果のテキスト
    """
    text = f"以下のテキストを簡潔にわかりやすく要約してください\n<text>\n{text}\n</text>"
    return _generate_response_(text)