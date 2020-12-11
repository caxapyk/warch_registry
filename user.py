from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash

from warch_registry.app import auth

users = {
    "reg": {
        "password": generate_password_hash("255"),
        "roles": ["manager"]
    }
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username).get("password"), password):
        return username


@auth.get_user_roles
def get_user_roles(username):
    return users.get(username).get("roles")


@auth.error_handler
def auth_error(status):
    return render_template("access_denied.html"), status
