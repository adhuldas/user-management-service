from pydantic import BaseModel, Field, field_validator
from constants.common_constants import CommonConstant



class SignOut(BaseModel):
    refresh_token: str = Field()

    @field_validator("refresh_token", check_fields=False)
    @classmethod
    def validate_files_id(cls, v, field):
        if not isinstance(v, str) or not v.strip():
            raise ValueError(CommonConstant.SUPPORTS_TEXT)
        return v