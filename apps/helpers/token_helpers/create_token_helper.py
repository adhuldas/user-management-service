"""
Module: create_token_helper.py

This module provides functionality for generating JWT access and refresh tokens
using the `flask_jwt_extended` library. It includes logic to set token expiry times
based on provided parameters and securely generate both types of tokens for authentication.

Classes:
    CreateToken: Handles the creation of JWT access and refresh tokens with custom expiration.

Dependencies:
    - datetime.timedelta
    - logging
    - flask_jwt_extended.create_access_token
    - flask_jwt_extended.create_refresh_token

Author: [Adhul Das M K]
Created: [2025-07-25]
"""

from datetime import timedelta
import logging
from flask_jwt_extended import create_access_token, create_refresh_token


class CreateToken:
    """
    A utility class for generating access and refresh JWT tokens.

    This class encapsulates the logic required to generate tokens with custom
    expiration times and error logging. It is used to support secure authentication
    in web APIs using JWT-based token mechanisms.
    """

    @staticmethod
    def create_access_refresh_token(additional_claims, hours=None):
        """
        Generate a JWT access token and refresh token for a user.

        Args:
            additional_claims (dict): Claims to be included in the JWT payload.
                Must include a 'user_details' dictionary containing a 'user_id'.
            hours (int, optional): If provided, sets token expiration in hours.
                Defaults to shorter expiration (10/12 minutes) if not set.

        Returns:
            tuple:
                str | bool: access_token or False if error
                str | bool: refresh_token or False if error
        """
        try:
            user_details = additional_claims.get("user_details")

            # Get token expiration durations
            access_token_time, refresh_token_time = (
                CreateToken.token_expiry_time(hours)
            )

            # Create the JWT access token
            access_token = create_access_token(
                user_details.get("user_id"),
                additional_claims=additional_claims,
                expires_delta=access_token_time,
            )

            # Create the JWT refresh token
            refresh_token = create_refresh_token(
                user_details.get("user_id"),
                additional_claims=additional_claims,
                expires_delta=refresh_token_time,
            )
            return access_token, refresh_token
        except Exception as exc:  # pragma: no cover
            logging.error(
                f"Error occured in function create_access_refresh_token,{exc}"
            )
            return False, False

    @staticmethod
    def token_expiry_time(hours=None):
        """
        Determine expiration times for access and refresh tokens.

        Args:
            hours (int, optional): Number of hours to set as expiration.
                If provided, sets access token for 12 hours and refresh token for 14 hours.
                If not, sets shorter durations of 10 and 12 minutes respectively.

        Returns:
            tuple:
                timedelta | bool: access_token_time or False if error
                timedelta | bool: refresh_token_time or False if error
        """
        try:
            if hours:
                # Longer expiry for access and refresh tokens
                access_token_time = timedelta(hours=12)
                refresh_token_time = timedelta(hours=14)
            else:
                # Shorter expiry for temporary usage
                access_token_time = timedelta(minutes=10)
                refresh_token_time = timedelta(minutes=12)
            return access_token_time, refresh_token_time
        except Exception as exc:
            logging.error(f"Error occured in function token_expiry_time:{exc}")
            return False, False
