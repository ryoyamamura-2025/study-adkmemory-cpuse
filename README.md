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
- Terminal: srcディレクトリ直下で `uv run python agent_execute.py`   

### フォルダ構成
```
src
├── agent_execute.py    # エージェントの実行
├── config.py           # 設定ファイル
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