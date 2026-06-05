# Mock pipeline for testing without API
from src.schemas import CompleteConfig, TableSchema, FieldDefinition, DataType, EndpointSchema, PageSchema, ComponentSchema, RoleSchema
from typing import Dict, Any

class MockPipeline:
    def run(self, user_input: str) -> Dict[str, Any]:
        # Create a mock config
        config = CompleteConfig(
            app_name="todo_app",
            database={
                "tables": [
                    TableSchema(
                        name="users",
                        fields=[
                            FieldDefinition(name="id", type=DataType.UUID, required=True),
                            FieldDefinition(name="email", type=DataType.STRING, required=True),
                            FieldDefinition(name="password", type=DataType.STRING, required=True)
                        ]
                    ),
                    TableSchema(
                        name="tasks",
                        fields=[
                            FieldDefinition(name="id", type=DataType.UUID, required=True),
                            FieldDefinition(name="title", type=DataType.STRING, required=True),
                            FieldDefinition(name="completed", type=DataType.BOOLEAN, required=True),
                            FieldDefinition(name="user_id", type=DataType.UUID, required=True)
                        ]
                    )
                ]
            },
            api={
                "endpoints": [
                    EndpointSchema(
                        path="/api/users",
                        method="POST",
                        request_body={"email": "string", "password": "string"},
                        response_body={"id": "uuid", "email": "string"},
                        auth_required=False,
                        roles_allowed=[]
                    ),
                    EndpointSchema(
                        path="/api/tasks",
                        method="GET",
                        request_body=None,
                        response_body={"tasks": "array"},
                        auth_required=True,
                        roles_allowed=["user"]
                    )
                ]
            },
            ui={
                "pages": [
                    PageSchema(
                        path="/login",
                        components=[
                            ComponentSchema(
                                name="login_form",
                                type="form",
                                props={"fields": ["email", "password"]},
                                data_source="/api/login"
                            )
                        ],
                        roles_allowed=[]
                    ),
                    PageSchema(
                        path="/dashboard",
                        components=[
                            ComponentSchema(
                                name="task_list",
                                type="table",
                                props={"columns": ["title", "completed"]},
                                data_source="/api/tasks"
                            )
                        ],
                        roles_allowed=["user"]
                    )
                ]
            },
            auth={
                "roles": [
                    RoleSchema(name="admin", permissions=["*"]),
                    RoleSchema(name="user", permissions=["tasks:read", "tasks:write"])
                ]
            },
            business_logic=[]
        )
        
        return {
            "success": True,
            "config": config.dict(),
            "execution_result": {
                "database_created": True,
                "api_generated": True,
                "ui_generated": True,
                "errors": []
            },
            "metrics": {
                "total_time_seconds": 0.5,
                "repair_attempts": 0,
                "stages_timing": {
                    "intent_parsing": 0.1,
                    "system_design": 0.1,
                    "schema_generation": 0.1,
                    "execution": 0.2
                },
                "success": True
            }
        }

# Test with mock
if __name__ == "__main__":
    pipeline = MockPipeline()
    result = pipeline.run("Build a todo app")
    print("Mock test successful!")
    print(f"App name: {result['config']['app_name']}")
    print(f"Database tables: {len(result['config']['database']['tables'])}")
    print(f"API endpoints: {len(result['config']['api']['endpoints'])}")
    print(f"UI pages: {len(result['config']['ui']['pages'])}")
