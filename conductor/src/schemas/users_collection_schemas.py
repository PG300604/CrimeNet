"""
Schemas for users resource input validation
"""
create_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 3,
            "maxLength": 16
        },
        "password": {"type": "string"},
        "role": {"type": "string"}
    },
    "required": ["username", "password", "role"]
}

list_users_schema = {
    "type": "object",
    "properties": {
        "users": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "role": {"type": "string"}
                },
                "required": ["username", "role"]
            }
        }
    },
    "required": ["users"]
}
