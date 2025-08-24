import logging
import secrets
import uuid
from apps.database.models import UserAccountOtpDb
from apps.validators.auth_validators import AuthValidator
from config import Config
from constants.token_expiry_constants import TokenExpireConstant


def create_dynamic_token(email, user_type, token_type="", user_details=None):
    """
    Generates a token  and stores it in the database with a slug ID.

    Args:
        email (str): User's email address.
        user_type (str): The type of user (e.g., admin, regular user).
        token_type (str): The token use-case, default is "signup".

    Returns:
        tuple: (token, slug_id) if successful, else (False, False).
    """
    try:
        # Generate a secure random token key
        dynamic_jwt = secrets.token_hex(16)
        # Generate a unique slug ID for the token
        slug_id = str(uuid.uuid4())

        # Validate email using regex
        regex = Config.EMAIL_REGEX_CHECK
        token = AuthValidator.email_regex_verify(
            regex,
            email,
            token_type,
            TokenExpireConstant.SIGNUP_TOKEN_EXPIRES,
            dynamic_jwt,
            user_details,
        )
        # Save the token data in the OTP collection
        otp_insert_data = {
            "jwt_key": dynamic_jwt,
            "slug_id": slug_id,
        }
        if user_type:
            otp_insert_data.update({"user_type": user_type})
        UserAccountOtpDb().insert_one(otp_insert_data)
        return token, slug_id

    except Exception as exc:
        logging.error(f"Error occurred in create_2fa: {exc}")
        return False, False
