# 包构造文件，创建程序实例
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	# from watchlist.models import User
    from models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'

@app.context_processor
def inject_user():
	# from watchlist.models import User
    from models import User
    user = User.query.first()
    return dict(user=user)

# from watchlist import views, errors, commands
# 为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。
# 同样的，load_user() 函数和 inject_user() 函数中使用的模型类也在函数内进行导入。
import views, errors, commands
