"""
Schemas for operations resource
"""
get_response = {
    "type": "object",
    "properties": {
        "taskData": {
            "type": "object",
            "properties": {
                "progress": {"type": "integer"},
                "createdDateTime": {"type": "string"},
                "lastActionDateTime": {"type": "string"},
                "status": {"type": "string"},
                "description": {"type": "string"},
                "result": {}
            },
            "required": ["createdDateTime", "lastActionDateTime", "status", "description"]
        }
    },
    "required": ["taskData"]
}
