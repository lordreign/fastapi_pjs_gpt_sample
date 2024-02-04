from enum import Enum


class ApiResult(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class PageOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


# logger name
class LoggerName(str, Enum):
    MAIN = "main"
    REQ = "request"
    RESP = "response"
    SQLALCHEMY = "sqlalchemy.engine"


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
