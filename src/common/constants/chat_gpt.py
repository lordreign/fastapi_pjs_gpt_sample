from enum import Enum


class ChatCompletionRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


# https://platform.openai.com/docs/models/model-endpoint-compatibility
class ChatCompletionModel(str, Enum):
    GPT4 = "gpt-4"
    GPT4_0613 = "gpt-4-0613"
    GPT4_32K = "gpt-4-32k"
    GPT4_32K_0613 = "gpt-4-32k-0613"
    GPT3_5_TURBO = "gpt-3.5-turbo"
    GPT3_5_TURBO_0613 = "gpt-3.5-turbo-0613"
    GPT3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT3_5_TURBO_16K_0613 = "gpt-3.5-turbo-16k-0613"


class CompletionsModel(str, Enum):
    TEXT_DAVINCI_003 = "text-davinci-003"
    TEXT_DAVINCI_002 = "text-davinci-002"
    TEXT_DAVINCI_001 = "text-davinci-001"
    TEXT_CURIE_001 = "text-curie-001"
    TEXT_BABBAGE_001 = "text-babbage-001"
    TEXT_ADA_001 = "text-ada-001"
    DAVINCI = "davinci"
    CURIE = "curie"
    BABBAGE = "babbage"
    ADA = "ada"
