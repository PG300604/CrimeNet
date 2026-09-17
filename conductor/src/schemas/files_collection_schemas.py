"""
Schemas for files collection
"""
files_list = {
    "type": "object",
    "properties": {
        "files": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["files"]
}
