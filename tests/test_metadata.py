from app.tools.remote.metadata_extractor import (
    fetch_openapi,
    extract_all_capabilities,
    get_capability_by_intent,
)

openapi = fetch_openapi()
caps = extract_all_capabilities(openapi)

print(caps)