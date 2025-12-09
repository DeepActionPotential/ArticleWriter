
from dataclasses import dataclass

@dataclass
class DefaultCFG:

    api_key: str = "YOUR-API"
    llm_model: str = "gemini/gemini-2.0-flash"

