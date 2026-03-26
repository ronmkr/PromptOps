from dataclasses import dataclass, field
from typing import Any


@dataclass
class PromptMetadata:
    description: str
    args_description: str = "Input Data"
    version: str = "1.0.0"
    last_updated: str = ""
    tags: list[str] = field(default_factory=list)
    sensitive: bool = False
    version_id: str | None = None
    path: str = ""


@dataclass
class PromptTemplate:
    metadata: PromptMetadata
    prompt: str | None = None
    system_prompt: str | None = None
    user_prompt: str | None = None
    raw_data: dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextProfile:
    name: str
    variables: dict[str, str]


@dataclass
class ChainStep:
    prompt_name: str
    input_vars: dict[str, str]
    output: str | None = None
    status: str = "pending"


@dataclass
class ChainResult:
    steps: list[ChainStep]
    final_output: str | None = None
    total_steps: int = 0
    completed_steps: int = 0
