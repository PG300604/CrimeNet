"""
User resource input validation
"""
get_schema = {
    "type": "object",
    "properties": {
        "role": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
    },
    "required": ["role"]
}

put_schema = {
    "type": "object",
    "properties": {
        "password": {"type": "string"},
        "role": {"type": "string"}
    },
    "required": ["password", "role"]
}

patch_schema = {
    "type": "object",
    "properties": {
        "password": {"type": "string"},
        "role": {"type": "string"}
    }
}
