import os
import logging
from logging.handlers import RotatingFileHandler
from src.common.constants.common import LoggerName


# logger 파일 폴더의 path
logger_folder_path = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 path
project_path = os.path.abspath(os.path.join(logger_folder_path, "..", ".."))
log_path = os.path.join(project_path, "logs", "main.log")

# logs 폴더가 없으면 생성
if not os.path.exists(os.path.join(project_path, "logs")):
    os.makedirs(os.path.join(project_path, "logs"))


def generate_logger(name: str, level: int, formatter: logging.Formatter, path: str = log_path) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # stream handler 설정
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # file handler 설정
    # file_handler = logging.FileHandler(os.path.join(project_path, "logs", f"{name}.log"), mode="w")
    file_handler = RotatingFileHandler(path, maxBytes=1024 * 1024 * 10, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


default_logger = generate_logger(
    name=LoggerName.MAIN.value,
    level=logging.DEBUG,
    formatter=logging.Formatter("%(asctime)s[%(levelname)s][%(lineno)s:%(pathname)s]: %(message)s"),
)

request_logger = generate_logger(
    name=LoggerName.REQ.value,
    level=logging.DEBUG,
    formatter=logging.Formatter(
        "%(asctime)s[%(levelname)s][%(name)s]: %(message)s \nhttpMethod: %(httpMethod)s,\nurl: %(url)s,\nheaders: %(headers)s,\nqueryParams: %(queryParams)s,\nbody: %(body)s"
    ),
)
response_logger = generate_logger(
    name=LoggerName.RESP.value,
    level=logging.DEBUG,
    formatter=logging.Formatter(
        "%(asctime)s[%(levelname)s][%(name)s]: %(message)s \nhttpMethod: %(httpMethod)s,\nurl: %(url)s,\nbody: %(body)s"
    ),
)
