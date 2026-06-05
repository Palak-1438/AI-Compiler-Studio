from typing import Dict, Any, Tuple
from openai import OpenAI
from src.config import QualityConfig, OPENAI_API_KEY
import json
import logging

logger = logging.getLogger(__name__)

class RepairEngine:
    def __init__(self, quality_config: QualityConfig):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.config = quality_config
        self.max_attempts = 3
    
    def repair(self, config: Dict, errors: list, stage: str) -> Tuple[Dict, bool]:
        for attempt in range(self.max_attempts):
            try:
                repaired = self._attempt_repair(config, errors, stage)
                
                from src.validator import Validator
                validator = Validator()
                is_valid, new_errors = validator.validate(repaired)
                
                if is_valid:
                    logger.info(f"Successfully repaired config after {attempt + 1} attempts")
                    return repaired, True
                
                errors = new_errors
                config = repaired
                
            except Exception as e:
                logger.error(f"Repair attempt {attempt + 1} failed: {e}")
        
        logger.error(f"Failed to repair after {self.max_attempts} attempts")
        return config, False
    
    def _attempt_repair(self, config: Dict, errors: list, stage: str) -> Dict:
        prompt = f"""
        Repair this configuration based on validation errors.
        
        STAGE: {stage}
        ERRORS: {json.dumps(errors, indent=2)}
        CURRENT CONFIG: {json.dumps(config, indent=2)}
        
        Fix all errors while preserving valid parts.
        Ensure all required fields are present:
        - app_name (string)
        - version (string)
        - database (object with 'tables' array)
        - api (object with 'endpoints' array)
        - ui (object with 'pages' array)
        - auth (object with 'roles' array)
        
        Return ONLY the repaired JSON configuration.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_size.value,
                temperature=self.config.temperature,
                messages=[
                    {"role": "system", "content": "You are a configuration repair expert. Fix errors precisely."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Repair attempt failed: {e}")
            # Return original config with minimal fixes
            if "app_name" not in config:
                config["app_name"] = "repaired_app"
            if "version" not in config:
                config["version"] = "1.0.0"
            if "database" not in config:
                config["database"] = {"tables": []}
            if "api" not in config:
                config["api"] = {"endpoints": []}
            if "ui" not in config:
                config["ui"] = {"pages": []}
            if "auth" not in config:
                config["auth"] = {"roles": []}
            return config
