import uuid
from pydantic import BaseModel, Field, constr
from typing import Optional, Dict, Union


class UserRegistrationModel(BaseModel):
    slug: str = Field(..., description="Slug ID from OTP DB")
    username: str = Field(
        ..., description="Username of the user (email or unique identifier)"
    )
    password: constr(min_length=8) = Field(
        ...,
        description="Password must meet regex pattern defined by PASSWORD_REGEX",
    )
    firstname: str = Field(..., description="First name of the user")
    lastname: str = Field(..., description="Last name of the user")
    timezone: str = Field(
        ..., description="Timezone of the user (e.g., Asia/Kolkata)"
    )
    token: Optional[str] = Field(
        None, description="JWT token passed for verification"
    )
    user_type: Optional[str] = Field(
        default="customer", description="Type of the user (e.g., customer, admin)"
    )
    context: Optional[str] = Field(
        None, description="Optional additional context for registration"
    )

    # Optional address fields if they are part of the _json payload
    country_code: Optional[str] = None
    phone_number: Optional[Union[str, int]] = None
    user_status: str = Field(default="")  # will be overridden by logic
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    def model_post_init(self, __context):
        if self.user_type == "customer":
            self.user_status = "Active"
        else:
            self.user_status = "Inactive"
