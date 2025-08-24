import re
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from config import Config
from constants.common_constants import CommonConstant


class SignupModel(BaseModel):
    email: str = Field()
    user_type: str = Field(default="customer")

    @field_validator(
        "email",
        "user_type",
        check_fields=False,
    )
    @classmethod
    def validate_non_empty_string(cls, v, field):
        if not isinstance(v, str) or not v.strip():
            raise ValueError(CommonConstant.SUPPORTS_TEXT)
        return v

    @field_validator("email", check_fields=False)
    @classmethod
    def validate_email(cls, v, info: ValidationInfo):
        if not isinstance(v, str):
            raise ValueError(CommonConstant.SUPPORTS_TEXT)
        hex_pattern = re.fullmatch(Config.EMAIL_REGEX_CHECK, v)
        if not hex_pattern:
            raise ValueError(CommonConstant.EMAIL_ID_NOT_VALID)

        return v
