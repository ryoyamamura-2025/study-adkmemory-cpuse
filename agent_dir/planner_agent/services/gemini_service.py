import os
from google import genai
from google.genai import types

from ..config import APPCONFIG

def generate_response(system_instruction, contents,
                      response_schema, model='gemini-2.5-flash'):
    # Geminiクライアント初期化
    _client = genai.Client(
        vertexai=True,
        project=APPCONFIG.GOOGLE_CLOUD_PROJECT,
        location=APPCONFIG.GOOGLE_CLOUD_LOCATION,
    )

    response = _client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            max_output_tokens=65535,
            response_mime_type='application/json',
            response_schema=response_schema,
        )
    )
    return '\n'.join(
        [p.text for p in response.candidates[0].content.parts if p.text]
    )