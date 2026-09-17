"""
Roles collection resource schemas
"""
create_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 16
        },
        "rank": {
            "type": "integer"
        }
    },
    "required": ["name", "rank"]
}

list_roles_schema = {
    "type": "object",
    "properties": {
        "roles": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "rank": {"type": "integer"}
                },
                "required": ["name", "rank"]
            }
        }
    },
    "required": ["roles"]
}
