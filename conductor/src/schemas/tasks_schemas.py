"""
Schemas for task resource
"""
from .network_schema import network_schema

post_input = {
    "type": "object",
    "properties": {
        "network": {
            "type": "array",
            "items": network_schema
        },
        "dataset": {"type": "string"},
        "options": {
            "type": "object",
            "properties": {
                "method": {"type": "string"},
                "parameters": {"type": "object"}
            },
            "required": ["method", "parameters"]
        },
        "parameters": {"type": "object"}
    }
}

network_construction_input = {
    "type": "object",
    "properties": {
        "network": {  # WP5 network
            "type": "object",
            "properties": {
                "conversations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "channels": {
                                "type": "array"
                            }
                        }
                    }
                },
                "voiceprintsMatrix": {"type": "object"}
            },
            "required": ["conversations", "voiceprintsMatrix"]
        },
        "threshold": {"type": "number"},
        "calibration": {"type": "boolean"},
        "directed": {"type": "boolean"}
    }
}
