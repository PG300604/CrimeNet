"""
Validation schemas for algorithm collection
"""
list_algorithms_schema = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "values": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "methods": {
                        "type": "array",
                        "values": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "parameter": {}
                            }
                        }
                    }
                }
            }
        }
    },
    "required": ["tasks"]
}
