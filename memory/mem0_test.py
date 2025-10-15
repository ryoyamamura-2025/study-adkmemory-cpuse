import os
from mem0 import Memory

from config import APPCONFIG


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

m = Memory.from_config(config)

messages = [
    {"role": "user", "content": "I'm planning to watch a movie tonight. Any recommendations?"},
    {"role": "assistant", "content": "How about thriller movies? They can be quite engaging."},
    {"role": "user", "content": "I'm not a big fan of thriller movies but I love sci-fi movies."},
    {"role": "assistant", "content": "Got it! I'll avoid thriller recommendations and suggest sci-fi movies in the future."}
]

# Store inferred memories (default behavior)
result = m.add(messages, user_id="alice", metadata={"category": "movie_recommendations"})

# Store memories with agent and run context
result = m.add(messages, user_id="alice", agent_id="movie-assistant", run_id="session-001", metadata={"category": "movie_recommendations"})

# Store raw messages without inference
result = m.add(messages, user_id="alice", metadata={"category": "movie_recommendations"}, infer=False)

all_memories = m.get_all(user_id="alice")
print(all_memories)

history = m.history(memory_id="e058205d-e4d9-4b82-b56e-128c7e5ceafe")
print(history)