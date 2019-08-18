from functools import wraps
from flask import session, url_for, redirect

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return wrapper 