"""
Schema for network nodes and edges
"""
network_schema = {
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["node"]
                },
                "id": {
                    "type": ["string", "integer"]
                },
                "properties": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"}
                    }
                }
            },
            "required": ["type", "id", "properties"]
        },
        {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["edge"]
                },
                "source": {"type": ["string", "integer"]},
                "target": {"type": ["string", "integer"]},
                "properties": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"}
                    }
                }
            },
            "required": ["type", "source", "target", "properties"]
        }
    ]
}

network_schema_v2 = {
    "type": "object",
    "properties": {
        "directed": {
            "type": "boolean"
        },
        "multigraph": {
            "type": "boolean"
        },
        "graph": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
                "version": {
                    "type": "number"
                },
                "id": {
                    "type": "string"
                }
            },
            "required": ["version", "id"]
        },
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string"
                    }
                },
                "required": ["id"]
            }
        },
        "links": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string"
                    },
                    "target": {
                        "type": "string"
                    }
                },
                "required": ["source", "target"]
            }
        }
    },
    "required": ["directed", "multigraph", "graph", "nodes", "links"]
}
