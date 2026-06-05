from typing import Dict, Any
from src.config import QualityConfig
from src.intent_parser import IntentParser
from src.system_designer import SystemDesigner
from src.schema_generator import SchemaGenerator
from src.validator import Validator
from src.repair_engine import RepairEngine
from src.executor import Executor
from src.schemas import CompleteConfig
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIPipeline:
    def __init__(self, quality_level: str = "balanced"):
        self.config = QualityConfig.get_cost_config(quality_level)
        self.intent_parser = IntentParser(self.config)
        self.system_designer = SystemDesigner(self.config)
        self.schema_generator = SchemaGenerator(self.config)
        self.validator = Validator()
        self.repair_engine = RepairEngine(self.config)
        self.executor = Executor()
        
        self.metrics = {
            "start_time": None,
            "end_time": None,
            "stages": {},
            "repair_attempts": 0,
            "success": False
        }
    
    def run(self, user_input: str) -> Dict[str, Any]:
        self.metrics["start_time"] = datetime.now()
        
        try:
            logger.info("Stage 1: Parsing intent...")
            stage_start = time.time()
            intent = self.intent_parser.parse(user_input)
            self.metrics["stages"]["intent_parsing"] = time.time() - stage_start
            
            logger.info("Stage 2: Designing system...")
            stage_start = time.time()
            architecture = self.system_designer.design_architecture(intent)
            self.metrics["stages"]["system_design"] = time.time() - stage_start
            
            logger.info("Stage 3: Generating schemas...")
            stage_start = time.time()
            config = self.schema_generator.generate_complete_config(intent, architecture)
            self.metrics["stages"]["schema_generation"] = time.time() - stage_start
            
            logger.info("Stage 4: Validating configuration...")
            is_valid, errors = self.validator.validate(config.dict())
            
            if not is_valid:
                logger.warning(f"Validation failed with {len(errors)} errors. Attempting repair...")
                self.metrics["repair_attempts"] += 1
                repaired_config, success = self.repair_engine.repair(config.dict(), errors, "complete_config")
                if success:
                    config = CompleteConfig(**repaired_config)
                    logger.info("Configuration repaired successfully")
            
            logger.info("Stage 5: Executing...")
            stage_start = time.time()
            execution_result = self.executor.execute(config)
            self.metrics["stages"]["execution"] = time.time() - stage_start
            
            self.metrics["success"] = True
            self.metrics["end_time"] = datetime.now()
            
            return {
                "success": True,
                "config": config.dict(),
                "execution_result": execution_result,
                "metrics": self._calculate_metrics()
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            self.metrics["success"] = False
            self.metrics["end_time"] = datetime.now()
            return {
                "success": False, 
                "error": str(e), 
                "metrics": self._calculate_metrics()
            }
    
    def _calculate_metrics(self) -> Dict:
        if self.metrics["start_time"] and self.metrics["end_time"]:
            duration = (self.metrics["end_time"] - self.metrics["start_time"]).total_seconds()
        else:
            duration = 0
        
        return {
            "total_time_seconds": duration,
            "repair_attempts": self.metrics["repair_attempts"],
            "stages_timing": self.metrics["stages"],
            "success": self.metrics["success"]
        }
