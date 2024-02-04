import os
import logging
from src.config.logger import generate_logger
from src.common.constants.common import LoggerName

config = {
    "name": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "db": os.getenv("DB_TARGET_DB"),
    "port": os.getenv("DB_PORT"),
}

# 설정이 누락되면 예외를 발생시킵니다.
for key, value in config.items():
    assert value is not None, f"Database config is not set in .env file: {key}"

from sqlalchemy import (
    create_engine,
    orm,
)  # pylint: disable=wrong-import-position, wrong-import-order

# sql logger 설정
sql_logger = generate_logger(
    name=LoggerName.SQLALCHEMY.value,
    level=logging.INFO,
    formatter=logging.Formatter("%(asctime)s[%(levelname)s][%(name)s]: %(message)s"),
)


def model_to_dict(obj):
    """Return the object's dict excluding private attributes,
    sqlalchemy state and relationship attributes.
    """
    excl = ("_sa_adapter", "_sa_instance_state")
    return {
        k: v
        for k, v in vars(obj).items()
        if not k.startswith("_") and not any(hasattr(v, a) for a in excl)
    }


class BaseModel(object):
    __abstract__ = True

    def __repr__(self):
        params = ", ".join(f"{k}={v}" for k, v in model_to_dict(self).items())
        return f"{self.__class__.__name__}({params})"


Base = orm.declarative_base(cls=BaseModel)


class EngineConn(object):
    __engine = None
    __Session = None

    def __init__(self):
        if self.__engine is None and self.__Session is None:
            self.__engine = self.__create_engine()
            self.__Session = self.__session_maker()

            # TODO model import 를 미리 선언해주어 관계 순서에 맞게 로드할 필요가 있다...
            # from src.models import (  # pylint: disable=unused-import, wrong-import-position
            # )

    def __create_engine(self):
        return create_engine(
            "{name}://{user}:{password}@{host}:{port}/{db}".format_map(config),
            connect_args={"connect_timeout": 10},
            # echo=True,
        )

    def __session_maker(self):
        return orm.sessionmaker(bind=self.__engine, autocommit=False, autoflush=False)

    def get_engine(self):
        return self.__engine

    def get_session(self):
        return self.__Session


def get_db():
    Session = EngineConn().get_session()  # pylint: disable=invalid-name
    db = Session()
    try:
        yield db
    finally:
        db.close()
