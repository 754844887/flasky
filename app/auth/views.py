from . import api_bp
from app.models import User
from flask_httpauth import HTTPBasicAuth
from flask import jsonify, g, make_response, request
from .form import RegisterForm
from app.models import db



auth = HTTPBasicAuth()


# 添加login_required后访问会回调这个方法
@auth.verify_password
def verify_password(email_or_token, password):
    print(2222)
    print(email_or_token)
    user = User.check_auth_token(email_or_token)
    if not user:
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.check_password(password):
            print(3333)
            return False    
    g.current_user = user
    return True

# 定义密码验证失败回调函数
@auth.error_handler
def auth_error():
    print(444455)
    return make_response(jsonify({'code': 403, 'data': {'message': '没有权限！'}}), 403)

@api_bp.route('/token', methods=['POST'])
@auth.login_required
def get_token():
    print(111)
    token = g.current_user.generate_auth_token()
    return jsonify({'code': 200, 'data': {'token': token.decode('ascii')}})
    
@api_bp.route('/register', methods=['POST'])
@auth.login_required
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'code': 400, 'info': '用户已存在！'})
        new_user = User(name=name, email=email)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'code': 200, 'info': '注册成功！'})
    return jsonify({'code': 400, 'info': form.errors})    
        



@api_bp.route('/')
@auth.login_required
def index():
    return 'index'

