from functools import wraps
from flask import g, make_response, jsonify
from .models import Permission


def permission_required(perm):
    def decorator(func):
        def decorator_function(*args, **kw):
            if not g.current_user.can(perm):
                return make_response(
                    jsonify({
                        'data': {},
                        'msg': "没有权限！",
                        'code': 403,
                        'extra': {}
                    }), 403)
            return func(*args, **kw)

        return decorator_function

    return decorator


def admin_required(func):
    return permission_required(Permission.ADMIN)(func)     