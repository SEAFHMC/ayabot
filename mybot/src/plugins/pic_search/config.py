from pydantic import Extra, BaseModel
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    saucenao_key: Optional[str] = ""


class ConfigError(Exception):
    pass
