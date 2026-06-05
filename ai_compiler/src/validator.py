from typing import Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)

class Validator:
    def __init__(self):
        pass
    
    def validate(self, config: Dict) -> Tuple[bool, List[str]]:
        errors = []
        
        required = ["app_name", "version", "database", "api", "ui", "auth"]
        for field in required:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Check database structure
        if "database" in config and "tables" not in config["database"]:
            errors.append("Database missing 'tables' field")
        
        # Check API structure
        if "api" in config and "endpoints" not in config["api"]:
            errors.append("API missing 'endpoints' field")
        
        # Check UI structure
        if "ui" in config and "pages" not in config["ui"]:
            errors.append("UI missing 'pages' field")
        
        # Check Auth structure
        if "auth" in config and "roles" not in config["auth"]:
            errors.append("Auth missing 'roles' field")
        
        errors.extend(self._check_consistency(config))
        
        return len(errors) == 0, errors
    
    def _check_consistency(self, config: Dict) -> List[str]:
        errors = []
        
        # Check UI components reference existing endpoints
        if "ui" in config and "pages" in config["ui"]:
            for page in config["ui"].get("pages", []):
                for component in page.get("components", []):
                    data_source = component.get("data_source")
                    if data_source:
                        endpoints = []
                        if "api" in config and "endpoints" in config["api"]:
                            endpoints = [e.get("path") for e in config["api"].get("endpoints", [])]
                        if data_source not in endpoints:
                            errors.append(f"UI component references non-existent endpoint: {data_source}")
        
        return errors
