EVALUATION_DATASET = [
    {"id": "real_001", "prompt": "Build a CRM with login, contacts, dashboard, and role-based access", "expected_success": True, "category": "real"},
    {"id": "real_002", "prompt": "Create an e-commerce platform with products and shopping cart", "expected_success": True, "category": "real"},
    {"id": "real_003", "prompt": "Build a task management app with teams and assignments", "expected_success": True, "category": "real"},
    {"id": "edge_vague_001", "prompt": "Build an app", "expected_success": False, "category": "vague"},
    {"id": "edge_vague_002", "prompt": "Make something with users", "expected_success": False, "category": "vague"},
    {"id": "edge_conflict_001", "prompt": "Build a public blog that requires login for all pages", "expected_success": False, "category": "conflicting"},
    {"id": "edge_incomplete_001", "prompt": "Build a social media platform", "expected_success": False, "category": "incomplete"},
]
