import os
import logging
import asyncio
import openai
from fastapi import WebSocket
from src.common.constants.common import LoggerName
from src.modules.chat_gpt import schema

openai.api_key = os.getenv("OPENAI_API_KEY")

log = logging.getLogger(LoggerName.MAIN.value)


def chat_completion(params: schema.ChatCompletionReq) -> schema.ChatAndCompletionsResp:
    result = openai.ChatCompletion.create(**params.model_dump(exclude_none=True))
    log.info("chat_completion result: %s", result)
    return result
    # return {
    #     "id": "chatcmpl-7ebtHBUfbbpSqPB2OiJtqYwSAISHX",
    #     "object": "chat.completion",
    #     "created": 1689913127,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": "\ud55c\uad6d\uc740 \ub3d9\uc544\uc2dc\uc544\uc5d0 \uc704\uce58\ud558\uace0 \uc788\uc2b5\ub2c8\ub2e4. \ubd81\ucabd\uc73c\ub85c\ub294 \ubd81\ud55c\uacfc \uc811\ud558\uba70, \ub3d9\ucabd\uc73c\ub85c\ub294 \ub3d9\ud574\ub85c\uc640 \ub3c4\ucfc4\ud574 \ud611\uacc4\uc120\uc744 \uacbd\uacc4\ub85c \uc77c\ubcf8\uacfc \ub9de\ub2ff\uc544 \uc788\uc73c\uba70, \uc11c\ucabd\uc73c\ub85c\ub294 \ud669\ud574\uc640 \uc811\ud558\uace0 \ub0a8\ucabd\uc73c\ub85c\ub294 \uc11c\ud574\uc640 \ub300\ud55c\ud574\ud611\uc744 \uc0ac\uc774\uc5d0 \ub450\uace0 \uc911\uad6d\uacfc \ub9de\ub2ff\uc544 \uc788\uc2b5\ub2c8\ub2e4.",
    #             },
    #             "finish_reason": "stop",
    #         }
    #     ],
    #     "usage": {"prompt_tokens": 20, "completion_tokens": 124, "total_tokens": 144},
    # }


async def chat_completion_stream(params: schema.ChatCompletionReq, websocket: WebSocket):
    result = openai.ChatCompletion.create(**params.model_dump(exclude_none=True), stream=True)
    completion_text = ""
    for event in result:
        if event["object"] == "chat.completion.chunk":
            # log.info("websocket_chat_completion event: %s", event)
            delta = event["choices"][0]["delta"]
            if delta.get("content", None) is None:
                break

            event_text = delta["content"]
            completion_text += event_text
            await websocket.send_text(event_text)
            # await manager.send_personal_message(event_text, websocket)
            await asyncio.sleep(
                0
            )  # https://websockets.readthedocs.io/en/stable/faq/asyncio.html#why-does-my-program-never-receive-any-messages
    log.info("websocket_chat_completion completion_text: %s", completion_text)


def completions(params: schema.CompletionsReq) -> schema.ChatAndCompletionsResp:
    result = openai.Completion.create(**params.model_dump(exclude_none=True))
    log.info("completions result: %s", result)
    return result
    # return {
    #     "id": "cmpl-7feHR2RO6tY2mGxBt0kjdxKMUPkTq",
    #     "object": "text_completion",
    #     "created": 1690160641,
    #     "model": "text-davinci-003",
    #     "choices": [
    #         {"text": "\n\n\ud55c\uad6d\uc740 \uc911\ub3d9", "index": 0, "logprobs": None, "finish_reason": "length"}
    #     ],
    #     "usage": {"prompt_tokens": 31, "completion_tokens": 15, "total_tokens": 46},
    # }
