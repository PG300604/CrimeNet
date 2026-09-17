"""
Schema for exception message
"""
exception_schema = {
    "type": "object",
    "properties": {
        "request_id": {"type": "string"},
        "code": {"type": "string"},
        "message": {"type": "string"},
        "target": {"type": "string"},
        "details": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "target": {"type": "string"},
                    "message": {"type": "string"}
                }
            }
        }
    }
}
