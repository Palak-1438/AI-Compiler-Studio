from src.pipeline import AIPipeline
from tests.test_dataset import EVALUATION_DATASET
import time
import json
from datetime import datetime

class TestPipeline:
    def run_evaluation(self):
        results = {"total": 0, "successful": 0, "failed": 0, "metrics": {"average_latency": 0}}
        total_latency = 0
        
        for test_case in EVALUATION_DATASET:
            print(f"\nRunning test: {test_case['id']}")
            pipeline = AIPipeline(quality_level="fast")
            
            start_time = time.time()
            result = pipeline.run(test_case["prompt"])
            latency = time.time() - start_time
            
            total_latency += latency
            results["total"] += 1
            
            if result["success"]:
                results["successful"] += 1
                print(f"  ✓ Success")
            else:
                results["failed"] += 1
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
            
            print(f"  Latency: {latency:.2f}s")
        
        if results["total"] > 0:
            results["metrics"]["average_latency"] = total_latency / results["total"]
        
        print("\n" + "="*50)
        print("EVALUATION RESULTS")
        print("="*50)
        print(f"Total tests: {results['total']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        print(f"Success rate: {results['successful']/results['total']*100:.1f}%")
        print(f"Average latency: {results['metrics']['average_latency']:.2f}s")
        
        return results

if __name__ == "__main__":
    test = TestPipeline()
    test.run_evaluation()
