from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config.env import check_openai_api_key
from src.config.database import EngineConn, Base

# openai api key 설정 확인
check_openai_api_key()

from src.modules.chat_gpt import controller as chat_gpt_controller  # pylint: disable=wrong-import-position


@asynccontextmanager
async def lifespan(application: FastAPI):
    # application 시작시
    application.state.models = {}
    engine_conn = EngineConn()
    Base.metadata.create_all(bind=engine_conn.get_engine())

    yield

    # application 종료시
    engine_conn.get_engine().dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(chat_gpt_controller.router)
