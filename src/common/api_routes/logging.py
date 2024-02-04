import logging
from typing import Any, Callable, Dict
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response
from src.common.constants.common import LoggerName

req_log = logging.getLogger(LoggerName.REQ.value)
resp_log = logging.getLogger(LoggerName.RESP.value)


class LoggingAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            await self._request_log(request)
            response: Response = await original_route_handler(request)
            self._response_log(request, response)
            return response

        return custom_route_handler

    @staticmethod
    def _has_json_body(request: Request) -> bool:
        if request.method in ("POST", "PUT", "PATCH") and request.headers.get("content-type") == "application/json":
            return True
        return False

    async def _request_log(self, request: Request) -> None:
        extra: Dict[str, Any] = {
            "httpMethod": request.method,
            "url": request.url.path,
            "headers": request.headers,
            "queryParams": request.query_params,
            "body": None,
        }

        if self._has_json_body(request):
            request_body = await request.body()
            extra["body"] = request_body.decode("UTF-8")

        req_log.info("", extra=extra)

    @staticmethod
    def _response_log(request: Request, response: Response) -> None:
        extra: Dict[str, str] = {
            "httpMethod": request.method,
            "url": request.url.path,
            # "body": response.body.decode("UTF-8"),
            "body": "표시안함",
        }

        resp_log.info("", extra=extra)
