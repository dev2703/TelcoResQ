from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./telcoresq.db")

# Vector Store
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/processed/faiss_index")
