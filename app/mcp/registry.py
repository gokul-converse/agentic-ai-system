SEND_EMAIL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Generate structured email details to send an email.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "Email address or name of recipient",
                },
                "subject": {
                    "type": "string",
                    "description": "Short professional subject line",
                },
                "body": {"type": "string", "description": "Professional email body"},
            },
            "required": ["recipient", "subject", "body"],
        },
    },
}

TOOL_REGISTRY = {"send_email": SEND_EMAIL_SCHEMA}
