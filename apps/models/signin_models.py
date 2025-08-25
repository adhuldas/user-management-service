from typing import Optional
from pydantic import BaseModel, Field, field_validator
from constants.common_constants import CommonConstant


class SignIn(BaseModel):
    username: str = Field()
    password: str = Field()
    location: Optional[str] = None

    @field_validator("username", "password", check_fields=False)
    @classmethod
    def validate_files_id(cls, v, field):
        if not isinstance(v, str) or not v.strip():
            raise ValueError(CommonConstant.SUPPORTS_TEXT)
        return v
