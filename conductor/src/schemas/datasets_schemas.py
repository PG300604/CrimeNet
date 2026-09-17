"""
Validation schemas for dataset resource
"""
from .network_schema import network_schema

post_input = {
    "type": "object",
    "properties": {
        "nodes": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "params": {}
    },
    "required": ["nodes"]
}

data_dto = {
    "type": "object",
    "properties": {
        "network": {
            "type": "array",
            "items": network_schema
        }
    },
    "required": ["network"]
}

delete_input = {
    "type": "object",
    "properties": {
        "edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "target": {"type": "string"}
                },
                "required": ["source", "target"]
            }
        },
        "nodes": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}

error_output = {
    "type": "object",
    "properties": {
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "success": {"type": "integer"},
                    "message": {"type": "string"},
                    "node": {"type": "string"},
                    "edge": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "target": {"type": "string"}
                        },
                        "required": ["source", "target"]
                    }
                },
                "required": ["success", "message"]
            }
        }
    },
    "required": ["errors"]
}
