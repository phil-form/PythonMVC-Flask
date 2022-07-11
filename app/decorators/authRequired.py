from functools import wraps
from sys import stderr
from flask import redirect, session, url_for

def authRequired(level="USER", orIsCurrentUser=False):
    def authRequireDecorator(func):
        @wraps(func)
        def functionWrapper(*args, **kwargs):
            if session.get('userroles') and level in session.get('userroles'):
                return func(*args, **kwargs)

            if orIsCurrentUser and session.get('userid') and session['userid'] == kwargs['userid']:
                return func(*args, **kwargs)

            return redirect(url_for('index'))

        return functionWrapper
    return authRequireDecorator