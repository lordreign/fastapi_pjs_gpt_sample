from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, model_validator
from src.common.constants.chat_gpt import ChatCompletionRole, ChatCompletionModel, CompletionsModel
from src.common import validators

# https://platform.openai.com/docs/api-reference/chat/create


class Message(BaseModel):
    role: ChatCompletionRole
    content: str
    name: Optional[str] = None
    function_call: Optional[str] = None

    class Config:
        use_enum_values = True


class Function(BaseModel):
    name: str
    description: Optional[str]
    parameters: dict[str, Any]


class ChatCompletionReq(BaseModel):
    model: Optional[ChatCompletionModel] = ChatCompletionModel.GPT3_5_TURBO.value
    messages: list[Message]
    functions: Optional[list[Function]] = None
    function_call: Optional[str | dict[str, Any]] = None  # functions중 결과로 어떤 function을 호출할지..
    temperature: Optional[int | float] = 1  # 0 ~ 2, 0보다크면 무작위 확율이 높아짐, top_p와 함께 사용하는 것 비추천
    top_p: Optional[int | float] = 1  # 0 ~ 1, 0.1일경우 top 10%의 결과만 고려됨
    n: Optional[int] = 1  # 질문당 몇개의 대답을 할지
    # stream: Optional[bool] = False # stream을 사용하게 될경우... 여기서는 api 기준이므로.. 제외 # 예제: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb
    stop: Optional[
        str | list[str]
    ] = None  # 멈추게 하고싶은 지점 설정, 최대 4개까지.. # 설명: https://help.openai.com/en/articles/5072263-how-do-i-use-stop-sequences
    max_tokens: Optional[int] = None  # math.inf  # 최대 생성하는 토큰 수
    presence_penalty: Optional[int | float] = 0  # 0이면 없음, -2 ~ 2, 비슷한 답변을 생성하게하는것을 막으려면 0 이상으로 설정
    frequency_penalty: Optional[int | float] = 0  # 0이면 없음, -2 ~ 2, 반복 답변을 생성하게하는것을 막으려면 0 이상으로 설정
    # logit_bias # 이해도가 낮아 일단 제외 # https://help.openai.com/en/articles/5247780-using-logit-bias-to-define-token-probability
    user: Optional[str] = None  # openai user id, 오용을 막고 monitoring을 위해 사용

    class Config:
        use_enum_values = True

    _validate_messages = validators.validate_field("messages", validators.check_min_length, 1)
    _validate_min_temperature = validators.validate_field("temperature", validators.check_min, 0)
    _validate_max_temperature = validators.validate_field("temperature", validators.check_max, 2)
    _validate_min_top_p = validators.validate_field("top_p", validators.check_min, 0)
    _validate_max_top_p = validators.validate_field("top_p", validators.check_max, 1)
    _validate_min_max_tokens = validators.validate_field("max_tokens", validators.check_min, 1)
    _validate_min_presence_penalty = validators.validate_field("presence_penalty", validators.check_min, -2)
    _validate_max_presence_penalty = validators.validate_field("presence_penalty", validators.check_max, 2)
    _validate_min_frequency_penalty = validators.validate_field("frequency_penalty", validators.check_min, -2)
    _validate_max_frequency_penalty = validators.validate_field("frequency_penalty", validators.check_max, 2)

    @model_validator(mode="after")
    def check_function_call(cls, data):
        if data.function_call and len(data.functions) == 0:
            raise ValueError("functions must be provided if function_call is provided")

        return data


class Choice(BaseModel):
    index: int
    finish_reason: str
    text: Optional[str] = None
    message: Optional[Message] = None
    logprobs: Optional[int | float] = None

    @model_validator(mode="after")
    def check_strip(cls, data):
        if data.text:
            data.text = data.text.strip()

        return data


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class ChatAndCompletionsResp(BaseModel):
    id: str
    object: str
    model: str
    created: datetime
    usage: Usage
    choices: list[Choice]


class CompletionsReq(BaseModel):
    model: Optional[CompletionsModel] = CompletionsModel.TEXT_DAVINCI_003.value
    prompt: str | list[str]
    suffix: Optional[str] = None
    max_tokens: Optional[int] = 16  # 최대 생성하는 토큰 수
    temperature: Optional[int | float] = 1  # 0 ~ 2, 0보다크면 무작위 확율이 높아짐, top_p와 함께 사용하는 것 비추천
    top_p: Optional[int | float] = 1  # 0 ~ 1, 0.1일경우 top 10%의 결과만 고려됨
    n: Optional[int] = 1  # prompt 마다 몇개의 대답을 할지
    # stream: Optional[bool] = False # stream을 사용하게 될경우... 여기서는 api 기준이므로.. 제외 # 예제: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb
    logprobs: Optional[int] = None  # max 5, 가능성이 높은 토큰과 선택한 토큰에 대한 로그 확률을 포함
    echo: Optional[bool] = False  # 프롬프트 echo back 여부
    stop: Optional[
        str | list[str]
    ] = None  # 멈추게 하고싶은 지점 설정, 최대 4개까지.. # 설명: https://help.openai.com/en/articles/5072263-how-do-i-use-stop-sequences
    presence_penalty: Optional[int | float] = 0  # 0이면 없음, -2 ~ 2, 비슷한 답변을 생성하게하는것을 막으려면 0 이상으로 설정
    frequency_penalty: Optional[int | float] = 0  # 0이면 없음, -2 ~ 2, 반복 답변을 생성하게하는것을 막으려면 0 이상으로 설정
    best_of: Optional[int] = 1  # 토큰당 가장 높은 로그 확률에 해당하는 녀석을 몇개 반환할지, max_tokens와 stop을 활용해야함 안그러면 돈많이 나옴
    # logit_bias # 이해도가 낮아 일단 제외 # https://help.openai.com/en/articles/5247780-using-logit-bias-to-define-token-probability
    user: Optional[str] = None  # openai user id, 오용을 막고 monitoring을 위해 사용

    _validate_min_temperature = validators.validate_field("temperature", validators.check_min, 0)
    _validate_max_temperature = validators.validate_field("temperature", validators.check_max, 2)
    _validate_min_top_p = validators.validate_field("top_p", validators.check_min, 0)
    _validate_max_top_p = validators.validate_field("top_p", validators.check_max, 1)
    _validate_min_max_tokens = validators.validate_field("max_tokens", validators.check_min, 1)
    _validate_min_presence_penalty = validators.validate_field("presence_penalty", validators.check_min, -2)
    _validate_max_presence_penalty = validators.validate_field("presence_penalty", validators.check_max, 2)
    _validate_min_frequency_penalty = validators.validate_field("frequency_penalty", validators.check_min, -2)
    _validate_max_frequency_penalty = validators.validate_field("frequency_penalty", validators.check_max, 2)

    class Config:
        use_enum_values = True
