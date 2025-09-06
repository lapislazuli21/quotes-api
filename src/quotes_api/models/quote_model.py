from pydantic import BaseModel, ConfigDict

# --- Pydantic Model ---
class Quote(BaseModel):
    id: int
    content: str
    author: int

    model_config = ConfigDict(from_attributes=True)

class QuoteCreate(BaseModel):
    content: str
    author: int