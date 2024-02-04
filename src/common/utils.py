import asyncio
import functools
from enum import Enum


async def launch_async(func, **kwargs) -> None:
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, functools.partial(func, **kwargs))


def enum_to_dict(enum_class: Enum) -> dict:
    return {item.name: item.value for item in enum_class}


def list_to_dict(item_list: list, key: str, value: str) -> dict:
    result = {}
    if item_list is not None and len(item_list) > 0:
        for item in item_list:
            result[item[key]] = item[value]
    return result


def dict_without_none(item: dict) -> dict:
    result = {}
    for key, value in item.items():
        if value is not None:
            if isinstance(value, dict):
                result[key] = dict_without_none(value)
            elif isinstance(value, list):
                value_list = []
                for v in value:
                    if isinstance(v, dict):
                        value_list.append(dict_without_none(v))
                    elif v is not None:
                        value_list.append(v)
                if len(value_list) > 0:
                    result[key] = value_list
            else:
                result[key] = value
    return result


def has_attr(item, attr: str) -> bool:
    try:
        getattr(item, attr)
        return True
    except AttributeError as e:
        print("AttributeError", e)
        return False


def has_value_in_enum(enumClass: Enum, value) -> bool:
    return value in set(item.value for item in enumClass)
