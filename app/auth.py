from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import current_app, request, g
from jose import jwt, JWTError

from .models import Customer, Mechanic


def _build_token(subject_id: int, role: str) -> str:
    payload = {
        "sub": str(subject_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc)
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


def encode_token(customer_id: int, is_admin: bool = False) -> str:
    role = "admin" if is_admin else "customer"
    return _build_token(customer_id, role)


def encode_mechanic_token(mechanic_id: int) -> str:
    return _build_token(mechanic_id, "mechanic")


def _decode_token_from_header():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header:
        return None, {"error": "Authorization header is missing."}, 401

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None, {"error": "Authorization header must be in the format: Bearer <token>."}, 401

    token = parts[1]

    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload, None, None
    except JWTError:
        return None, {"error": "Invalid or expired token."}, 401
    except Exception:
        return None, {"error": "Authentication failed."}, 401


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload, error_body, status_code = _decode_token_from_header()
        if error_body:
            return error_body, status_code

        role = payload.get("role")
        subject_id = payload.get("sub")

        if role not in ("customer", "admin", "mechanic") or subject_id is None:
            return {"error": "Invalid token payload."}, 401

        try:
            subject_id = int(subject_id)
        except ValueError:
            return {"error": "Invalid token subject."}, 401

        if role in ("customer", "admin"):
            user = Customer.query.get(subject_id)
            if not user:
                return {"error": "Customer not found."}, 404
        elif role == "mechanic":
            user = Mechanic.query.get(subject_id)
            if not user:
                return {"error": "Mechanic not found."}, 404
        else:
            return {"error": "Invalid role."}, 401

        g.current_user = user
        g.current_user_id = subject_id
        g.current_role = role

        return f(*args, **kwargs)

    return decorated


def roles_required(*allowed_roles):
    def wrapper(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            if g.current_role not in allowed_roles:
                return {"error": "You are not authorized to access this route."}, 403
            return f(*args, **kwargs)
        return decorated
    return wrapper


def admin_required(f):
    @wraps(f)
    @roles_required("admin")
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated