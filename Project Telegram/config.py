from dotenv import load_dotenv
import os

load_dotenv()

# Telegram
API_ID   = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CANAL_ID = int(os.getenv("CANAL_ID"))

# LLMs
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
GROQ_MODEL     = "llama-3.1-8b-instant"

# Herramientas
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_MAX_RESULTS = 2