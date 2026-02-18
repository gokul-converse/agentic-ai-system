from typing import Any, Dict, List, Optional

import requests

from app.utils.logger import logger

OPENAPI_URL = "http://localhost:8001/openapi.json"


INTENT_MAP = {
    ("POST", "/leave/"): "apply_leave",
    ("POST", "/personal/employees"): "create_employee",
    ("GET", "/leave/calender"): "get_leave_calendar",
    ("POST", "/admin/roles"): "create_role",
    ("GET", "/employee/employees"): "get_all_employees",
    ("GET", "/leave/pending/leave"): "get_pending_leaves",
    ("GET", "/leave/details"): "get_upcoming_leaves",
}

# Fetch OpenAPI


def fetch_openapi() -> Dict[str, Any]:
    logger.info("[METADATA] Fetching OpenAPI spec")

    try:
        response = requests.get(OPENAPI_URL, timeout=10)
        response.raise_for_status()
        logger.info("[METADATA] OpenAPI fetched successfully")
        return response.json()

    except Exception:
        logger.exception("[METADATA ERROR] Failed to fetch OpenAPI")
        raise


# Extract capabilities


def extract_all_capabilities(openapi_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    logger.info("[METADATA] Extracting capabilities from OpenAPI")

    capabilities = []
    paths = openapi_json.get("paths", {})

    try:
        for path, methods in paths.items():
            for method, details in methods.items():
                method_upper = method.upper()

                key = (method_upper, path)
                if key not in INTENT_MAP:
                    continue

                intent = INTENT_MAP[key]

                request_body = details.get("requestBody")
                if not request_body:
                    continue

                content = request_body.get("content", {})
                json_schema = content.get("application/json", {}).get("schema", {})

                if "$ref" not in json_schema:
                    continue

                schema_name = json_schema["$ref"].split("/")[-1]

                capabilities.append(
                    {
                        "intent": intent,
                        "method": method_upper,
                        "path": path,
                        "schema": schema_name,
                        "description": details.get(
                            "summary", intent.replace("_", " ").title()
                        ),
                    }
                )

        logger.info(f"[METADATA] Extracted {len(capabilities)} capabilities")
        return capabilities

    except Exception:
        logger.exception("[METADATA ERROR] Failed extracting capabilities")
        raise


# Find capability by intent


def get_capability_by_intent(
    capabilities: List[Dict[str, Any]], intent: str
) -> Optional[Dict[str, Any]]:

    logger.info(f"[METADATA] Searching capability for intent={intent}")

    for cap in capabilities:
        if cap["intent"] == intent:
            logger.info("[METADATA] Capability found")
            return cap

    logger.warning("[METADATA] Capability not found")
    return None


# Extract schema fields


def extract_form_fields_from_schema(
    openapi_json: Dict[str, Any], schema_name: str
) -> List[Dict[str, Any]]:

    logger.info(f"[METADATA] Extracting form fields for schema={schema_name}")

    schemas = openapi_json.get("components", {}).get("schemas", {})

    if schema_name not in schemas:
        logger.error("[METADATA ERROR] Schema not found in OpenAPI")
        raise ValueError(f"Schema {schema_name} not found")

    schema = schemas[schema_name]

    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])

    form_fields = []

    for field_name, field_info in properties.items():
        field_type = field_info.get("type", "string")

        if field_type == "string" and field_info.get("format") == "date":
            field_type = "date"

        form_fields.append(
            {
                "name": field_name,
                "type": field_type,
                "required": field_name in required_fields,
            }
        )

    logger.info(f"[METADATA] Extracted {len(form_fields)} form fields")

    return form_fields
