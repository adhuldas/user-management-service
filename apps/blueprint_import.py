from apps.routes.auth_route import (
    auth_module,
)  # pylint:disable=import-outside-toplevel
from apps.routes.user_route import (
    user_module,
)  # pylint:disable=import-outside-toplevel

__all__ = [
    "auth_module",
    "user_module",
]