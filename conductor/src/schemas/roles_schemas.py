"""
Input validation schemas for roles
"""
role_info = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 16
        },
        "rank": {
            "type": "integer",
            "minimum": 0
        }
    }
}

role_create = {
    "type": "object",
    "properties": {
        "rank": {
            "type": "integer",
            "minimum": 0
        }
    },
    "required": ["rank"]
}
