import hashlib
import secrets
from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user, login_required  # noqa: F401 - re-exported for routes.py


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password, password_hash):
    return secrets.compare_digest(hash_password(password), password_hash)


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Доступ дозволено тільки адміністратору.")
            return redirect(url_for("index"))
        return view(*args, **kwargs)
    return wrapped_view
