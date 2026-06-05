from typing import Dict, Any
from openai import OpenAI
from src.config import QualityConfig, OPENAI_API_KEY
import json
import logging

logger = logging.getLogger(__name__)

class SystemDesigner:
    def __init__(self, quality_config: QualityConfig):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.config = quality_config
    
    def design_architecture(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Based on these requirements, design the system architecture:
        
        INTENT: {json.dumps(intent, indent=2)}
        
        Generate architecture with:
        1. Database schema (tables, relationships)
        2. API endpoints (RESTful structure)
        3. UI pages and navigation flow
        4. Authentication and authorization model
        
        Output STRICT JSON:
        {{
            "database_design": {{
                "tables": [
                    {{"name": "users", "fields": ["id", "email", "password"]}}
                ]
            }},
            "api_design": {{
                "endpoints": [
                    {{"path": "/api/users", "methods": ["GET", "POST"]}}
                ]
            }},
            "ui_design": {{
                "pages": ["login", "dashboard"],
                "layout": "sidebar"
            }},
            "auth_design": {{
                "roles": ["admin", "user"],
                "permission_matrix": {{}}
            }}
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_size.value,
                temperature=self.config.temperature,
                messages=[
                    {"role": "system", "content": "You are a system architect. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"System design failed: {e}")
            return {
                "database_design": {"tables": []},
                "api_design": {"endpoints": []},
                "ui_design": {"pages": ["dashboard"], "layout": "sidebar"},
                "auth_design": {"roles": ["admin", "user"], "permission_matrix": {}}
            }
