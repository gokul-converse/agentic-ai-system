from pydantic import BaseModel

class TextInput(BaseModel):
    text: str



"""
For file uploads we usually don’t use Pydantic body model.
FastAPI handles files directly.

So you don’t need to add a request model here.

(Your earlier text APIs needed it. Document upload doesn’t.)
"""

class ChatRequest(BaseModel):
    message: str