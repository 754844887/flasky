from . import api_bp
from app.models import User, Role, Host
from flask_httpauth import HTTPBasicAuth
from flask import jsonify, g, make_response, request
from .form import RegisterForm
from app.models import db
import json

auth = HTTPBasicAuth()


# 添加login_required后访问会回调这个方法
@auth.verify_password
def verify_password(email_or_token, password):
    user = User.check_auth_token(email_or_token)
    if not user:
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.current_user = user
    return True


# 定义密码验证失败回调函数
@auth.error_handler
def auth_error():
    return make_response(
        jsonify({
            'data': {},
            'msg': "没有权限！",
            'code': 403,
            'extra': {}
        }), 403)


@api_bp.route('/token', methods=['POST'])
@auth.login_required
def get_token():
    username = g.current_user.name
    token = g.current_user.generate_auth_token()
    return jsonify({
            'data': {
                'token': token.decode('ascii'),
                'username': username
                },
            'msg': "登录成功！",
            'code': 200,
            'extra': {}
    })


@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_data()
    json_data = json.loads(data.decoindexde('utf-8'))
    name = json_data['name']
    email = json_data['email']
    password = json_data['password']
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            'data': {},
            'msg': "用户已存在！",
            'code': 400,
            'extra': {}
            })
    new_user = User(name=name, email=email)
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
           'data': {},
            'msg': "注册成功！",
            'code': 200,
            'extra': {}
            })


@api_bp.route('/hosts')
@auth.login_required
def get_host_list():
    hosts = Host.query.all()
    return 'index'
