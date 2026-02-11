## worked perfect when we have azure alone, now trying to integrate both azure and gemini

# import os
# from openai import AzureOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# _client = None

# def get_llm():
#     """
#     Returns the Azure Openai client
#     """
#     global _client

#     if _client is None:
#         _client = AzureOpenAI(
#             api_key=os.getenv("AZURE_AI_KEY"),
#             azure_endpoint=os.getenv("AZURE_AI_ENDPOINT"),
#             api_version=os.getenv("AZURE_OPENAI_API_VERSION")
#         )

#     return _client


import os
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

_client = None          # No client yet, before running the first time

def get_llm():
    global _client

    if _client is not None:             # If LLM client was already created once, just reuse it
        return _client

    provider = os.getenv("LLM_PROVIDER", "azure")       # Look for LLM_PROVIDER in .env, If not found → default to "azure"

    logger.info(f"[LLM INIT] Initializing LLM provider={provider}")

    try:
        if provider == "azure":
            from openai import AzureOpenAI

            _client = AzureOpenAI(
                api_key=os.getenv("AZURE_AI_KEY"),
                azure_endpoint=os.getenv("AZURE_AI_ENDPOINT"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION")
            )

            logger.info("[LLM INIT SUCCESS] Azure client created")

        elif provider == "gemini":
            from google import genai

            _client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )

            logger.info("[LLM INIT SUCCESS] Gemini client created")

        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

        return _client
    
    except Exception:
        logger.exception(f"[LLM INIT ERROR] Failed to initialize provider={provider}")
        raise


