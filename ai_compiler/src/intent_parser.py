import json
from typing import Dict, Any
from openai import OpenAI
from src.config import QualityConfig, OPENAI_API_KEY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentParser:
    def __init__(self, quality_config: QualityConfig):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.config = quality_config
    
    def parse(self, user_input: str) -> Dict[str, Any]:
        prompt = f"""
        Extract structured application requirements from user input.
        
        USER INPUT: "{user_input}"
        
        OUTPUT STRICT JSON with these fields:
        {{
            "app_type": "CRM|E-commerce|Analytics|Social|Other",
            "core_features": ["list", "of", "main", "features"],
            "entities": ["User", "Contact", "Product"],
            "roles": ["admin", "user", "premium"],
            "business_rules": [],
            "data_models": [],
            "ambiguous_requirements": [],
            "confidence_score": 0.95
        }}
        
        Return ONLY valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_size.value,
                temperature=self.config.temperature,
                messages=[
                    {"role": "system", "content": "You are a precise requirements analyzer. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Parsed intent: {result.get('app_type', 'unknown')}")
            return result
        except Exception as e:
            logger.error(f"Intent parsing failed: {e}")
            # Return a default structure
            return {
                "app_type": "Unknown",
                "core_features": [],
                "entities": ["User"],
                "roles": ["admin", "user"],
                "business_rules": [],
                "data_models": [],
                "ambiguous_requirements": ["Unable to parse requirements"],
                "confidence_score": 0.5
            }
