"""
Schemas for login input validation
"""
login_request = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "password"]
}

login_response = {
    "type": "object",
    "properties": {
        "accessToken": {"type": "string"}
    },
    "required": ["accessToken"]
}
