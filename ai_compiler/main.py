from src.pipeline import AIPipeline
from tests.test_pipeline import TestPipeline
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="AI Compiler System")
    parser.add_argument("--prompt", type=str, help="Natural language prompt")
    parser.add_argument("--evaluate", action="store_true", help="Run evaluation suite")
    parser.add_argument("--quality", choices=["fast", "balanced", "high"], default="balanced")
    
    args = parser.parse_args()
    
    if args.evaluate:
        print("Running evaluation suite...")
        test = TestPipeline()
        results = test.run_evaluation()
    elif args.prompt:
        print(f"Processing: {args.prompt}")
        pipeline = AIPipeline(quality_level=args.quality)
        result = pipeline.run(args.prompt)
        print(json.dumps(result, indent=2))
    else:
        print("Please provide --prompt or --evaluate")

if __name__ == "__main__":
    main()
