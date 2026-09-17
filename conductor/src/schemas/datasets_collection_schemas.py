"""
Schemas for dataset collection
"""
list_datasets = {
    "type": "object",
    "properties": {
        "datasets": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["datasets"]
}


create_dataset = {
    "type": "object",
    "properties": {
        "datasetName": {
            "type": "string",
            "minLength": 3,
            "maxLength": 16
        },
        "datasetDescription": {"type": "string"},
        "uploadFile": {"type": "string"},
        "dumpFile": {"type": "string"}
    },
    "required": ["datasetName"]
}


delete_dataset = {
    "type": "object",
    "properties": {
        "datasetName": {
            "type": "string"
        }
    },
    "required": ["datasetName"]
}
