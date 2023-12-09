import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass
class CompletionConfig:
    model: str
    messages: List[dict]
    temperature: float = 0.7
    max_tokens: Optional[float] = None
    response_format: Optional[dict] = None
    seed: Optional[int] = None
    tools: Optional[List] = None
    tool_choice: Optional[str] = None

    def unique_hash(self) -> str:
        """Generate a unique hash for the configuration."""
        data = asdict(self)
        canonical_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(canonical_string.encode()).hexdigest()
