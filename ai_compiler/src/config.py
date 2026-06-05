from enum import Enum
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class ModelSize(str, Enum):
    FAST = "gpt-3.5-turbo"
    BALANCED = "gpt-4-turbo-preview"
    ACCURATE = "gpt-4"

class QualityConfig(BaseModel):
    """Quality vs Cost tradeoff configuration"""
    model_size: ModelSize = ModelSize.BALANCED
    max_retries: int = 3
    temperature: float = 0.1
    repair_attempts: int = 2
    timeout_seconds: int = 30
    
    @classmethod
    def get_cost_config(cls, quality_level: str = "balanced") -> "QualityConfig":
        configs = {
            "fast": QualityConfig(model_size=ModelSize.FAST, temperature=0.0, max_retries=1),
            "balanced": QualityConfig(model_size=ModelSize.BALANCED, temperature=0.1, max_retries=2),
            "high": QualityConfig(model_size=ModelSize.ACCURATE, temperature=0.05, max_retries=3)
        }
        return configs.get(quality_level, configs["balanced"])

OPENAI_API_KEY = os.getenv("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", "")
