from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from enum import Enum

class DataType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    JSON = "json"
    UUID = "uuid"

class FieldDefinition(BaseModel):
    name: str
    type: DataType
    required: bool = True
    unique: bool = False
    foreign_key: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None

class TableSchema(BaseModel):
    name: str
    fields: List[FieldDefinition]
    primary_key: str = "id"
    indexes: List[str] = []

class EndpointSchema(BaseModel):
    path: str
    method: str
    request_body: Optional[Dict[str, Any]]
    response_body: Dict[str, Any]
    auth_required: bool = True
    roles_allowed: List[str] = []
    rate_limit: Optional[int] = None

class ComponentSchema(BaseModel):
    name: str
    type: str
    props: Dict[str, Any]
    data_source: Optional[str] = None

class PageSchema(BaseModel):
    path: str
    components: List[ComponentSchema]
    roles_allowed: List[str] = []

class RoleSchema(BaseModel):
    name: str
    permissions: List[str]
    parent_role: Optional[str] = None

class BusinessRule(BaseModel):
    name: str
    condition: str
    action: str
    applies_to: List[str]

class CompleteConfig(BaseModel):
    app_name: str
    version: str = "1.0.0"
    database: Dict[str, List[TableSchema]] = Field(default_factory=dict)
    api: Dict[str, List[EndpointSchema]] = Field(default_factory=dict)
    ui: Dict[str, List[PageSchema]] = Field(default_factory=dict)
    auth: Dict[str, List[RoleSchema]] = Field(default_factory=dict)
    business_logic: List[BusinessRule] = Field(default_factory=list)
