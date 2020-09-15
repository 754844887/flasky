from flask import Flask
import config
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    from .models import db
    db.init_app(app)
    
    from .auth import api_bp
    app.register_blueprint(api_bp)

    csrf = CSRFProtect()
    csrf.init_app(app)

    cors = CORS()
    cors.init_app(app)
    
    return app


app = create_app()
# 生产csrf_token 用于表单csrf验证
# @app.after_request
# def after_request(response):
#     csrf_token = generate_csrf()
#     response.set_cookie('csrf_token', csrf_token) 
#     return response   