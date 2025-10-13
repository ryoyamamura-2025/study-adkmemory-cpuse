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
agent_dir
├── agent_app.py            # エージェントの実行
├── credentials.json        # Google Cloud の認証情報
├── deploy-to-engine.py     # デプロイ用スクリプト
├── planner_agent           # Agent本体
│   ├── __init__.py
│   ├── agent.py            # root_agentの定義
│   ├── config.py           # 設定ファイル
│   ├── services            # 各種モジュール
│   │   └── gemini_service.py
│   └── tools               # Agent が利用できるツール群
│       └── llm_tools.py    # Gemini (LLM) を使ったツール
└── test.py
```

## Mem0
LLM アプリケーションの Memory Layer を構築できる OSS のフレームワーク  
ローカル実行でデータの永続化を試す  
コードは `memory` に配置

### 環境構築
1. データベース
    - データ永続化用のベクトルデータベースに PostgreSQL (pgvector拡張) を使用  
    - ローカル開発では docker でコンテナを起動
    ```
    cd memory
    docker compose up -d
    ```

2. LLM/Embedding Model
    - Vertex AI を利用。LLM は標準でインテグレーションが用意されていないので、litellm 経由で利用

3. 上記を Mem0 インスタンス化時の `config` として設定
```json
config = {
    "llm": {
        "provider": "litellm",
        "config": {
            "model": "vertex_ai/gemini-2.5-flash",
            "temperature": 0.0,
            "max_tokens": 2000,
        },
    },
    "embedder": {
        "provider": "vertexai",
        "config": {
            "model": "gemini-embedding-001",
            "embedding_dims": 1536,
            "memory_add_embedding_type": "RETRIEVAL_DOCUMENT",
            "memory_update_embedding_type": "RETRIEVAL_DOCUMENT",
            "memory_search_embedding_type": "RETRIEVAL_QUERY"
        },
    },
    "vector_store": {
        "provider": "pgvector",
        "config": {
            "user": "dev_user",
            "password": "dev_password",
            "host": "localhost",
            "port": "5432",
        }
    },
}
```

### Memory の CRUD 操作
[Python SDK Quickstart](https://docs.mem0.ai/open-source/python-quickstart#advanced)を参照  
デフォルトでは、`postgres`データベースに以下のテーブルが作成される。

| Schema | Name           | Type  | Owner    |
|--------|----------------|-------|----------|
| public | mem0           | table | dev_user |
| public | mem0migrations | table | dev_user |

mem0migrationsは変更履歴と考えられる。変更履歴は `.history()` で確認できる。

## Vertex AI Memory Bank 
Google が提供する Agent の長期記憶のためのマネージドサービス  
ADK における状態・記憶[一番わかり易い解説記事](https://cloud.google.com/blog/ja/topics/developers-practitioners/remember-this-agent-state-and-memory-with-adk)と[実装例](https://github.com/GoogleCloudPlatform/devrel-demos/tree/main/ai-ml/python-tutor)  
`agent_dir/python_tutor_agent`配下で実装

### 環境構築
Memory Bank を利用するには Vertex AI Agent Engine が前提。  
`deploy-to-engine.py` を参考に Agent を指定しない空の Engine をデプロイし、そこに Memory だけ保存していく
あとの実装は上記記事とコードを参照

### Context/Session/State/Event 等についてのメモ
Agent は一連のやり取りを Context という Object で管理している。  
Context が最上位の（最も多くの）情報を持った Object。Context には、Session が含まれており、Session には State や Event が含まれる。  

以下は Session Object の例
```
id='199ccf11-5f89-4632-bb3d-00226a6d381d' app_name='python_tutor_agent' user_id='user' 
state={'hoge': 'hogehoge', 'fuga': 'fugafuga, ...} 
events=[
    Event(content=Content(parts=[Part(text='こんにちは'),], role='user'),...,
    Event(content=Content(parts=[Part(text="""こんにちは、ジョンさん！😊 お帰りなさい！✨まず、ジョンさんのお名前を記憶させてくださいね。""",…,
                                 Part(function_call=FunctionCall(args={'name': 'John'}, id='XXX', name='set_user_name')),], role='model'),...,
]
...
```

## 参考サイト
### Agent Development Kit
- [クイックスタート: Agent Development Kit でエージェントをビルドする](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart?hl=ja)
- [【超速報】Agent Development Kit で会話型エージェントを作成する](https://zenn.dev/google_cloud_jp/articles/1b1cbd5318bdfe)
- [Agent Development Kitによるエージェント開発入門](https://speakerdeck.com/enakai00/agent-development-kit-niyoruezientokai-fa-ru-men) 
- [ADK を使用したエージェントの状態と記憶](https://cloud.google.com/blog/ja/topics/developers-practitioners/remember-this-agent-state-and-memory-with-adk)

### Mem0
- [Python SDK Quickstart](https://docs.mem0.ai/open-source/python-quickstart#advanced)
- [Pgvector](https://docs.mem0.ai/components/vectordbs/dbs/pgvector)
- [REST API Server](https://docs.mem0.ai/open-source/features/rest-api#pull-from-docker-hub)

### Pgvector
- [pgvectorとDockerでベクトルデータベースの実験環境構築](https://takumi-oda.com/blog/2025/04/27/post-4500/)

### Memory Bank