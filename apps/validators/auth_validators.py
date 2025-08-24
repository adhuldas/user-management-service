import datetime
import logging
import re
import uuid

import jwt
import pytz
from apps.database.models import UsersTokenDb
from constants.common_constants import CommonConstant


class AuthValidator:
    """ """

    @staticmethod
    def rating_limiting_email(email, type_of_token, expire_minute=None):
        """
        Enforces rate-limiting on email-based token requests by checking DB logs.

        Parameters
        ----------
        email : str
            User's email address.
        type_of_token : str
            The type of token (e.g., 'signup', '2FA') being requested.
        expire_minute : int, optional
            Time window in minutes to enforce rate-limiting (default is 60).

        Returns
        -------
        bool
            True if the user has exceeded the allowed number of attempts, False otherwise.
        """
        try:
            expire_minute = expire_minute or 60
            return_type = False

            # Retrieve previous token assignment data from DB
            get_assigned_token = UsersTokenDb().find_one(
                {"email": email, "type": type_of_token},
                {"_id": 0, "assigned_time": 1, "attempt": 1},
            )

            if get_assigned_token:
                assigned_token_time = get_assigned_token.get("assigned_time")
                attempt = get_assigned_token.get("attempt")

                if not assigned_token_time or not attempt:
                    return return_type

                # Convert string timestamps to datetime
                current_time = datetime.datetime.now()
                current_time = datetime.datetime.strptime(
                    str(current_time), "%Y-%m-%d %H:%M:%S.%f"
                )
                assigned_time_expire = datetime.datetime.strptime(
                    assigned_token_time, "%Y-%m-%d %H:%M:%S.%f"
                ) + datetime.timedelta(minutes=expire_minute)

                # If still within expiry window and attempts exceed limit
                if (
                    current_time <= assigned_time_expire
                    and attempt >= CommonConstant.MAX_ATTEMPT
                ):
                    return True

            return return_type

        except Exception as exc:
            logging.error(f"Error occurred in function rating_limiting_email: {exc}")
            return False

    @staticmethod
    def user_exist_check_mail(user_lower=None):
        """
        Returns a user-exists error message for registration validations.

        Parameters
        ----------
        user_lower : bool, optional
            If True, returns a more descriptive error message.

        Returns
        -------
        str
            A string describing the user existence error.
        """
        try:
            if user_lower:
                return (
                    "A user with a similar email address already exists. "
                    "Please create a new email address to sign up for the app."
                )
            else:
                return "This user already exists"
        except Exception as exc:
            logging.error(f"Error occurred in function user_exist_check_mail: {exc}")

    def email_regex_verify(
        regex,
        email,
        token_type,
        token_expire_time,
        jwt_secret_key,
        user_details=None,
    ):
        """
        Validates the email against a regex pattern and manages token creation and rate-limiting.

        Parameters
        ----------
        regex : str
            Regex pattern used to validate the email format.
        email : str
            Email address being validated.
        token_type : str
            Type of token being generated (e.g., 'signup', '2FA').
        token_expire_time : timedelta
            Expiration time for the generated JWT.
        jwt_secret_key : str
            Secret key used for JWT signing.
        user_details : dict, optional
            Additional payload for the JWT (used when token_type != 'signup').

        Returns
        -------
        str or bool
            The generated token if email is valid, else False.
        """
        try:
            # Validate email format using regex
            if re.fullmatch(regex, email):
                # Create standard JWT claims
                additional_claims = {
                    "fresh": False,
                    "iat": datetime.datetime.now(pytz.utc),
                    "jti": str(uuid.uuid4()),
                    "type": "access",
                    "sub": email,
                    "nbf": datetime.datetime.now(pytz.utc),
                    "exp": datetime.datetime.now(pytz.utc) + token_expire_time,
                }

                # Add token-type-specific claims
                if token_type in ["signup", "2FA", "delete_account"]:
                    additional_claims.update({"email": email, "id": "0"})
                else:
                    additional_claims.update({"user_details": user_details})
                # Generate JWT token
                token = jwt.encode(
                    additional_claims,
                    jwt_secret_key,
                    algorithm="HS256",
                )

                # Check for existing token document
                user_exist = UsersTokenDb().find_one(
                    {"email": email, "type": token_type},
                    {"_id": 0, "attempt": 1},
                )
                if user_exist is None:
                    # First-time token creation
                    UsersTokenDb().insert_one(
                        {
                            "token": token,
                            "email": email,
                            "type": token_type,
                            "assigned_time": str(datetime.datetime.now()),
                            "attempt": 1,
                        }
                    )
                else:
                    # Increment attempt count if less than max
                    attempt = user_exist.get("attempt", 0)
                    attempt = attempt + 1 if attempt < CommonConstant.MAX_ATTEMPT else 1
                    # Update token and attempt in DB
                    UsersTokenDb().find_one_and_update(
                        {"email": email, "type": token_type},
                        {
                            "token": token,
                            "assigned_time": str(datetime.datetime.now()),
                            "attempt": attempt,
                        },
                    )
                return token
            else:
                return False

        except Exception as exc:
            logging.error(f"Error occurred in email_regex_verify: {exc}")
            return False
