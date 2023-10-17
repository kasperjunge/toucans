import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Union


@dataclass
class ChatAPIConfig:
    model: str
    temperature: float
    messages: List[str]
    functions: List[str] = None
    function_call: Union[str, None] = None
    max_tokens: Union[int, None] = None
    frequency_penalty: Union[float, None] = None
    logit_bias: Dict[str, float] = None
    presence_penalty: Union[float, None] = None
    top_p: Union[float, None] = None
    n: Union[int, None] = None
    stop: Union[str, List[str], None] = None
    stream: Union[bool, None] = None
    user: Optional[str] = None

    def unique_hash(self) -> str:
        """Generate a unique hash for the configuration."""
        # Convert the dataclass instance to a dictionary
        data = asdict(self)

        # Convert the dictionary to a canonical JSON string.
        # This ensures that the order of keys won't affect the resulting hash.
        canonical_string = json.dumps(data, sort_keys=True)

        # Compute the SHA-256 hash of this string
        return hashlib.sha256(canonical_string.encode()).hexdigest()
