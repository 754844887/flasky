from . import api_bp
from app.models import User, Role, Host
from flask_httpauth import HTTPBasicAuth
from flask import jsonify, g, make_response, request
from .form import RegisterForm
from app.models import db
import json
from app.decorators import admin_required, permission_required

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
            'msg': "帐号或密码错误！",
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
    json_data = json.loads(data.decode('utf-8'))
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


# 添加/删除权限
@api_bp.route('/edit_role', methods=['PUT'])
@auth.login_required
@admin_required
def edit_role():
    result = {
            'data': {},
            'msg': "",
            'code': "",
            'extra': {}
            }
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    role_name = json_data['role']
    user_id = json_data['user_id']  
    user = User.query.filter_by(id=user_id).first()
    if not user:
        result['msg'] = "用户不存在！"
        result['code'] = 404
        return jsonify(result)
    user.role = Role.query.filter_by(name=role_name).first()
    db.session.add(user)
    db.session.commit()
    result['msg'] = "修改权限成功！"
    result['code'] = 200
    return jsonify(result)    


