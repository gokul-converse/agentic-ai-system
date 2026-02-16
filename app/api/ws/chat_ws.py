from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import requests

from app.agents.orchestrator import OrchestratorAgent
from app.tools.remote.metadata_extractor import (
    fetch_openapi,
    extract_all_capabilities,
    get_capability_by_intent,
    extract_form_fields_from_schema,
)
from app.tools.local.form_transformer import FormTransformer
from app.utils.logger import logger
from app.services.message_enhancer import enhance_message
from app.agents.domain.knowledge_agent import KnowledgeAgent
from app.agents.domain.email_agent import EmailAgent

router = APIRouter()

knowledge_agent = KnowledgeAgent()
email_agent = EmailAgent()

# Initialize once (module level = good for performance)
orchestrator = OrchestratorAgent()
form_transformer = FormTransformer()



openapi_spec = fetch_openapi()
capabilities = extract_all_capabilities(openapi_spec)

# this is for not running 8001 env - it should work for those who dont want HR actions.. in that case also this file should run
def is_hr_service_available():
    try:
        requests.get("http://localhost:8001/health", timeout=2)
        return True
    except:
        return False
    
# -----------------------------
# WebSocket Endpoint
# -----------------------------
@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):

    await websocket.accept()
    logger.info("[WS] Client connected")

    try:
        while True:
            data = await websocket.receive_json()

            # FIRST: HANDLE TOOL EXECUTION - User clicks send, FE sends execute tool , BE detects type == execute tool, calls mcp, mcp calls BE mail api, return sucess, BE sends success message
            # ---------------------------------- execute_tool → goes to MCP
            if data.get("type") == "execute_tool":

                tool_name = data.get("tool")
                arguments = data.get("data")

                logger.info(f"[WS] Executing tool via MCP: {tool_name}")

                try:
                    response = requests.post(
                        "http://localhost:9000/execute",
                        json={
                            "tool_name": tool_name,
                            "arguments": arguments
                        },
                        timeout=25
                    )

                    response.raise_for_status()
                    result = response.json()

                    await websocket.send_json({
                        "type": "message",
                        "text": result.get("message", "Tool executed successfully.")
                    })

                except Exception as e:
                    logger.exception("[WS] MCP execution failed")
                    await websocket.send_json({
                        "type": "message",
                        "text": "Failed to execute tool."
                    })

                continue

            # HANDLE NORMAL CHAT
            user_message = data.get("message")

            if not user_message:
                await websocket.send_json({
                    "type": "message",
                    "text": "Empty message received."
                })
                continue

            # -----------------------------
            # Orchestrator decides
            # -----------------------------
            orch = orchestrator.process(user_message)

            # -----------------------------
            # CASE 1: General chat
            # -----------------------------
            if orch.type == "chat":
                await websocket.send_json({
                    "type": "message",
                    "text": orch.reply
                })
                continue


            # CASE 3: Knowledge Query (RAG-based answer)

            if orch.type == "knowledge":
                result = knowledge_agent.answer(user_message)

                # await websocket.send_json({
                #     "type": "message",
                #     "text": result["answer"]
                # })

                await websocket.send_json({
                "type": "knowledge",
                "answer": result["answer"],
                "sources": result["sources"]
            })
                continue

            # -----------------------------
            # CASE 4: Business Intent (Form / API Action)
            # -----------------------------
            if orch.type == "intent":

                intent = orch.intent
                logger.info(f"[WS] Intent detected: {intent}")

                # Add Email Intent Handling
                if intent == "send_email":
                    result = email_agent.generate_email(user_message)

                    if result.get("type") == "confirm_email":
                        await websocket.send_json({
                        "type": "tool",
                        "tool": "send_email",
                        "text": result["data"]
                    })
                    else:
                        await websocket.send_json({
                            "type": "message",
                            "text": result.get("message", "Failed to generate email.")
                        })

                    continue


                # ---- Special read-only APIs ----

                if intent == "get_leave_calendar":

                    if not is_hr_service_available():
                        await websocket.send_json({
                            "type": "message",
                            "text": "HR service is not running in this environment."
                        })
                        continue

                    try:
                        resp = requests.get("http://localhost:8001/leave/calender", timeout=5)
                        resp.raise_for_status()

                        await websocket.send_json({
                            "type": "table",
                            "text": resp.json()
                        })
                    except Exception:
                        await websocket.send_json({
                            "type": "message",
                            "text": "Failed to fetch leave calendar."
                        })
                    continue

                if intent == "get_all_employees":
                    if not is_hr_service_available():
                        await websocket.send_json({
                            "type": "message",
                            "text": "HR service is not running in this environment."
                        })
                        continue
                    
                    try:
                        resp = requests.get("http://localhost:8001/employee/employees")
                        resp.raise_for_status()

                        await websocket.send_json({
                            "type": "table",
                            "text": resp.json()
                        })
                    except Exception:
                        await websocket.send_json({
                            "type": "message",
                            "text": "Failed to fetch employee list."
                        })
                    continue

                if intent == "get_pending_leaves":
                    if not is_hr_service_available():
                        await websocket.send_json({
                            "type": "message",
                            "text": "HR service is not running in this environment."
                        })
                        continue
                                    
                    try:
                        resp = requests.get("http://localhost:8001/leave/pending/leave")

                        if resp.status_code == 404:
                            backend_msg = resp.json().get(
                                "detail",
                                "You have no pending leave requests."
                            )

                            enhanced_msg = enhance_message(backend_msg)

                            await websocket.send_json({
                                "type": "message",
                                "text": enhanced_msg
                            })
                            continue

                        resp.raise_for_status()

                        await websocket.send_json({
                            "type": "table",
                            "text": resp.json()
                        })

                    except Exception:
                        await websocket.send_json({
                            "type": "message",
                            "text": "Failed to fetch pending leaves."
                        })

                    continue

                if intent == "get_upcoming_leaves":
                    if not is_hr_service_available():
                        await websocket.send_json({
                            "type": "message",
                            "text": "HR service is not running in this environment."
                        })
                        continue

                    try:
                        resp = requests.get("http://localhost:8001/leave/details")

                        if resp.status_code == 404:
                            backend_msg = resp.json().get(
                                "detail",
                                "No leave details found."
                            )

                            enhanced_msg = enhance_message(backend_msg)

                            await websocket.send_json({
                                "type": "message",
                                "text": enhanced_msg
                            })
                            continue

                        resp.raise_for_status()

                        leaves = resp.json()

                        approved_leaves = [
                            leave for leave in leaves
                            if leave.get("status") == "approved"
                        ]

                        if approved_leaves:
                            await websocket.send_json({
                                "type": "table",
                                "text": approved_leaves
                            })
                        else:
                            enhanced_msg = enhance_message(
                                "You do not have any approved upcoming leaves."
                            )

                            await websocket.send_json({
                                "type": "message",
                                "text": enhanced_msg
                            })

                    except Exception:
                        await websocket.send_json({
                            "type": "message",
                            "text": "Failed to fetch leave details."
                        })

                    continue


                # ---- Default → Generate Form ----

                capability = get_capability_by_intent(capabilities, intent)

                if not capability:
                    await websocket.send_json({
                        "type": "message",
                        "text": "Sorry, I can't handle this request yet."
                    })
                    continue

                raw_fields = extract_form_fields_from_schema(
                    openapi_spec,
                    capability["schema"]
                )

                schema_form = {
                    "intent": intent,
                    "action": {
                        "method": capability["method"],
                        "path": capability["path"]
                    },
                    "fields": raw_fields
                }

                try:
                    ui_form = form_transformer.transform(schema_form)
                except Exception:
                    logger.exception("[WS] FormTransformer failed, sending raw schema")
                    ui_form = schema_form

                if ui_form.get("type") != "form":
                    logger.warning("[WS] Form response missing type=form, patching")
                    ui_form["type"] = "form"

                await websocket.send_json(ui_form)
                continue

            # -----------------------------
            # Fallback
            # -----------------------------
            await websocket.send_json({
                "type": "message",
                "text": "Sorry, I didn’t understand that."
            })

    except WebSocketDisconnect:
        logger.info("[WS] Client disconnected")