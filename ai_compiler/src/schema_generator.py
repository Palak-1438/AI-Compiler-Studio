from typing import Dict, Any
from src.schemas import CompleteConfig, TableSchema, FieldDefinition, DataType, EndpointSchema, PageSchema, ComponentSchema, RoleSchema, BusinessRule
from openai import OpenAI
from src.config import QualityConfig, OPENAI_API_KEY
import json
import logging

logger = logging.getLogger(__name__)

class SchemaGenerator:
    def __init__(self, quality_config: QualityConfig):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.config = quality_config
    
    def generate_complete_config(self, intent: Dict, architecture: Dict) -> CompleteConfig:
        prompt = f"""
        Generate complete application configuration.
        
        INTENT: {json.dumps(intent, indent=2)}
        ARCHITECTURE: {json.dumps(architecture, indent=2)}
        
        Output MUST match this schema structure:
        {{
            "app_name": "todo_app",
            "version": "1.0.0",
            "database": {{
                "tables": [
                    {{
                        "name": "users",
                        "fields": [
                            {{"name": "id", "type": "uuid", "required": true}},
                            {{"name": "email", "type": "string", "required": true}}
                        ]
                    }}
                ]
            }},
            "api": {{
                "endpoints": [
                    {{
                        "path": "/api/users",
                        "method": "GET",
                        "request_body": null,
                        "response_body": {{"type": "object"}},
                        "auth_required": true,
                        "roles_allowed": ["admin"],
                        "rate_limit": null
                    }}
                ]
            }},
            "ui": {{
                "pages": [
                    {{
                        "path": "/dashboard",
                        "components": [],
                        "roles_allowed": ["user"]
                    }}
                ]
            }},
            "auth": {{
                "roles": [
                    {{"name": "admin", "permissions": ["*"]}}
                ]
            }},
            "business_logic": []
        }}
        
        Return ONLY valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_size.value,
                temperature=self.config.temperature,
                messages=[
                    {"role": "system", "content": "You are a precise configuration generator. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            config_dict = json.loads(response.choices[0].message.content)
            return CompleteConfig(**config_dict)
        except Exception as e:
            logger.error(f"Schema generation failed: {e}")
            # Return a minimal valid config
            return CompleteConfig(
                app_name="generated_app",
                database={"tables": []},
                api={"endpoints": []},
                ui={"pages": []},
                auth={"roles": []}
            )
