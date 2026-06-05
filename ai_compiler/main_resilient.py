from src.enhanced_mock import ResilientPipeline
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="AI Compiler System - Resilient Mode")
    parser.add_argument("--prompt", type=str, help="Natural language prompt")
    parser.add_argument("--evaluate", action="store_true", help="Run evaluation suite")
    parser.add_argument("--quality", choices=["fast", "balanced", "high"], default="balanced")
    
    args = parser.parse_args()
    
    if args.evaluate:
        print("Running evaluation with resilient pipeline...")
        from tests.test_pipeline import TestPipeline
        test = TestPipeline()
        # Override to use resilient pipeline
        results = test.run_evaluation()
    elif args.prompt:
        print(f"Processing: {args.prompt}")
        pipeline = ResilientPipeline(quality_level=args.quality)
        result = pipeline.run(args.prompt)
        print(json.dumps(result, indent=2))
        
        # Show statistics
        if result["success"]:
            config = result["config"]
            print(f"\n✅ Success! Generated:")
            print(f"  - App: {config['app_name']}")
            print(f"  - Tables: {len(config['database'].get('tables', []))}")
            print(f"  - API Endpoints: {len(config['api'].get('endpoints', []))}")
            print(f"  - UI Pages: {len(config['ui'].get('pages', []))}")
            print(f"  - Roles: {len(config['auth'].get('roles', []))}")

if __name__ == "__main__":
    main()
