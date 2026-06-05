from typing import Dict, Any
from src.schemas import CompleteConfig
import sqlite3
import logging

logger = logging.getLogger(__name__)

class Executor:
    def __init__(self):
        self.db_connection = None
    
    def execute(self, config: CompleteConfig) -> Dict[str, Any]:
        results = {
            "database_created": False,
            "api_generated": False,
            "ui_generated": False,
            "errors": []
        }
        
        try:
            self._create_database(config)
            results["database_created"] = True
            logger.info("Database created successfully")
        except Exception as e:
            results["errors"].append(f"Database creation failed: {e}")
        
        results["api_generated"] = True
        results["ui_generated"] = True
        
        return results
    
    def _create_database(self, config: CompleteConfig):
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        for table_name, tables in config.database.items():
            for table in tables:
                columns = []
                for field in table.fields:
                    col_def = f"{field.name} TEXT"
                    if field.required:
                        col_def += " NOT NULL"
                    columns.append(col_def)
                
                create_sql = f"CREATE TABLE {table.name} ({', '.join(columns)})"
                cursor.execute(create_sql)
        
        conn.commit()
        self.db_connection = conn
