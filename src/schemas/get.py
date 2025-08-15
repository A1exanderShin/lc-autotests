GET_DEMO_SLOT_ID_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {"type": "number"},
        "codeText": {"type": "string"},
        "status": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "slotUrl": {"type": "string", "format": "uri"}
            },
            "required": ["slotUrl"]
        }
    },
    "required": ["code", "codeText", "status", "data"]
}
