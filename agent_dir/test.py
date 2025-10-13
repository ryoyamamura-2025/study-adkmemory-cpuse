from google import genai
from google.genai import types
import myself_agent.services.gemini_service as gem
import json

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
parts.append(types.Part.from_text(text=f'神戸旅行の計画を立てて'))
contents=[types.Content(role='user', parts=parts)]

response = gem.generate_response(system_instruction="あなたは優秀なアシスタントです", contents=contents, response_schema=response_schema)

text = """{
  "title": "神戸満喫！港町と異国情緒、美食を巡る旅",
  "summary": "美しい港の景色、異国情緒あふれる街並み、そして絶品の神戸牛を堪能する2日間の神戸旅行プランです。歴史的な建造物から最新のショッピングエリア、そして癒しの温泉まで、神戸の魅力を存分に味わえます。",
  "timeline": "1日目:午前中に神戸到着後、ホテルにチェックイン。午後はメリケンパークで神戸ポートタワーや海洋博物館を見学し、港の雰囲気を満喫。その後、南京町で中華街の活気と食べ歩きを楽しみます。夕食は三宮・元町エリアで本場の神戸牛を堪能。夜はライトアップされた港の夜景を眺めながら散策。2日目:午前中は北野異人館街を散策し、異国情緒あふれる洋館巡り。午後は六甲山へ向かい、ケーブルカーで山頂へ。展望台から神戸の街並みや大阪湾を一望します。その後、有馬温泉へ移動し、日帰り入浴で旅の疲れを癒します。夕食は有馬温泉街で地元の料理を味わうか、神戸市内に戻って別のグルメを楽しむことも可能です。"
}"""

print(type(text))

aaa = '\n'.join(
    [text]
)

bbb = '\n'.join(
    [p.text for p in response.candidates[0].content.parts if p.text]
)

print(aaa)
print("-----------")
print(bbb)
print("-----------")
print(json.loads(bbb))
print(type(json.loads(bbb)))
print("-----------")
print(response.parsed)
print(type(response.parsed))