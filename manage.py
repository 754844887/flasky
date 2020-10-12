"""
使用flask_migrate和flask_script插件初始化数据库
需执行完如下三条命令才会在数据库中生成对应的表
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.models import db
from app.models import User, Role


app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



@manager.option('-n', '--name')
@manager.option('-e', '--email')
@manager.option('-p', '--password')
def create_user(name, email, password):
    user = User(name, email)
    user.password = password
    db.session.add(user)
    db.session.commit()
    print('创建用户成功！')

@manager.command   
def init_role():
    Role.insert_roles()
    print('初始化权限成功！')




if __name__ == '__main__':
    manager.run()