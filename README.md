# Agentの技術習得用リポジトリ
Google Agent Development Kit (ADK), LangGraph, Mem0 の技術習得用リポジトリ

## Agent Development Kit
### 環境構築
uv で仮想環境を構築
```
# git clone後
uv init
uv venv
uv sync
```

### 実行方法
- Web UI: srcディレクトリ直下で `uv run adk web`   
- Terminal: srcディレクトリ直下で `uv run python agent_app.py`   
    - Local か Remote かでスクリプトを変えること
    - Remote の場合は リソースID を環境変数に設定すること

### デプロイ
デプロイする Agent に設定を変更して実行
```
cd src
uv run python deploy-to-engine.py 
```

### フォルダ構成
```
src
├── agent_app.py        # エージェントの実行
├── config.py           # 設定ファイル
├── deploy-to-engine.py # デプロイ
├── planner_agent       # Agent本体
│   ├── __init__.py
│   └── agent.py
├── services
│   └── gemini_service.py   # gemini 実行関数
└── tools               # Agent が利用できるツール群
    └── llm_tools.py    # Gemini (LLM) を使ったツール
```


## 参考サイト
- [クイックスタート: Agent Development Kit でエージェントをビルドする](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart?hl=ja)
- [【超速報】Agent Development Kit で会話型エージェントを作成する](https://zenn.dev/google_cloud_jp/articles/1b1cbd5318bdfe)
- [Agent Development Kitによるエージェント開発入門](https://speakerdeck.com/enakai00/agent-development-kit-niyoruezientokai-fa-ru-men) 