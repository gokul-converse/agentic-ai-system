from app.tools.remote.metadata_extractor import (
    extract_all_capabilities,
    fetch_openapi,
    get_capability_by_intent,
)

openapi = fetch_openapi()
caps = extract_all_capabilities(openapi)

print(caps)
