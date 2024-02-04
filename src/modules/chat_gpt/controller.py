import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.common.schemas import response_schema
from src.common.constants.common import LoggerName
from src.common.api_routes import logging as logging_api_routes
from src.config.websocket_manager import WebsocketManager
from src.modules.chat_gpt import service, schema

log = logging.getLogger(LoggerName.MAIN.value)
manager = WebsocketManager()

router = APIRouter(
    prefix="/chat_gpt",
    tags=["chat_gpt"],
    route_class=logging_api_routes.LoggingAPIRoute,
    responses={404: {"message": "Not found"}},
)


@router.post(
    "/chat_completion",
    response_model=response_schema.ResponseBase[schema.ChatAndCompletionsResp],
    summary="ChatGPT chat completion api call",
)
def chat_completion(params: schema.ChatCompletionReq):
    return {"data": service.chat_completion(params)}


@router.websocket("/chat_completion/ws")
async def chat_completion_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            content = await websocket.receive_text()
            if content:
                params = schema.ChatCompletionReq(messages=[{"role": "user", "content": content.strip()}])
                await service.chat_completion_stream(params, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post(
    "/completions",
    response_model=response_schema.ResponseBase[schema.ChatAndCompletionsResp],
    summary="ChatGPT completions api call",
)
def completions(params: schema.CompletionsReq):
    return {"data": service.completions(params)}
