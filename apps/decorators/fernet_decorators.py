import ast
from functools import wraps
import logging
from flask import json, jsonify, request
from cryptography.fernet import Fernet
from config import Config
from constants.response_constants import ResponseConstants

fernet = Fernet(Config.FERNET_KEY)


def encrypt_or_decrypt(action, fernet, data):
    try:
        if fernet:
            if action == "encrypt":
                return fernet.encrypt(data)
            elif action == "decrypt":
                return fernet.decrypt(data).decode()
        return None
    except Exception as exc:
        logging.error(f"Error occured in function encrypt_or_decrypt:{exc}")
        return None


def encryptor(func):
    """
    FOR ENCRYPTING DATA
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            response_data = func(
                *args, **kwargs
            )  # Calling function to get response data
            if isinstance(response_data, dict) or isinstance(response_data, list):
                json_data = json.dumps(response_data)
                encrypted_data = encrypt_or_decrypt(
                    "encrypt", fernet, json_data.encode()
                )
                if encrypted_data is None:
                    return jsonify(message=ResponseConstants.UNPROCESSABLE_ENTITY), 422
                response_data = {"data": encrypted_data.decode("utf-8")}, 200
        except Exception as exc:  # pragma: no cover
            # Handle encryption errors here
            logging.error(f"Encryption error:{exc}")

        return response_data

    return wrapped


def decryptor(func):
    """
    FOR DECRYPTING DATA
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            encrypted_data = None
            # getting encrypted data from request parameter
            if request.json:
                encrypted_data = request.json
            # check if data is not null
            if encrypted_data:
                data = encrypted_data.get("data")
                decrypted_data = encrypt_or_decrypt("decrypt", fernet, data)
                if decrypted_data is None:
                    return jsonify(message=ResponseConstants.UNPROCESSABLE_ENTITY), 422

                # append decoded data as request object
                if decrypted_data:

                    request.decrypted_data = ast.literal_eval(decrypted_data)

                else:  # pragma: no cover
                    return (
                        jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE),
                        500,
                    )
        except Exception as exc:
            # Handle decryption errors here
            logging.error(f"Decryption error: {exc}")
            return (
                jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE),
                500,
            )

        return func(*args, **kwargs)

    return wrapped
