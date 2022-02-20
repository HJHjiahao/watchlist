# print(1) https://github.com/greyli/flask-tutorial/blob/master/chapters
from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev' # further consideration
# chapter 2 Hello https://github.com/greyli/flask-tutorial/blob/master/chapters/c2-hello.md
# http://127.0.0.1:5000   http://localhost:5000 
'''
@app.route('/') # consistent with the tail of link
# @app.route('/home')
def hello():
    # return 'Welcome to My Watchlist!'
    # return 'port'
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    
# set FLASK_ENV=development  /production

from flask import escape, url_for
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'
    
'''

# chapter 3 templates https://github.com/greyli/flask-tutorial/blob/master/chapters/c3-template.md
'''
name = 'hhhhhh'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)
'''

# chapter 4 Static https://github.com/greyli/flask-tutorial/blob/master/chapters/c4-static.md
'''
name = 'hhhhhh'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)
'''
# 如果你对 CSS 很头疼，可以借助前端框架来完善页面样式，比如 Bootstrap、Semantic-UI、Foundation 等。
# 它们提供了大量的 CSS 定义和动态效果，使用起来非常简单。
# 扩展 Bootstrap-Flask 可以简化在 Flask 项目里使用 Bootstrap 4 的步骤。
# https://github.com/greyli/bootstrap-flask

# chapter 5 Database https://github.com/greyli/flask-tutorial/blob/master/chapters/c5-database.md
# SQlite  使用 SQLAlchemy——一个 Python 数据库工具（ORM，即对象关系映射）。
# 借助 SQLAlchemy，你可以通过定义 Python 类来表示数据库里的一张表（类属性表示表中的字段 / 列）
# 通过对这个类进行各种操作来代替写 SQL 语句。这个类我们称之为模型类，类中的属性我们将称之为字段。
# 可使用一个叫做 Flask-SQLAlchemy 的官方扩展来集成 SQLAlchemy pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app

# Flask 提供了一个统一的接口来写入和获取这些配置变量：Flask.config 字典。
# 配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前
# 据库文件的名称和后缀你可以自由定义，一般会使用 .db、.sqlite 和 .sqlite3 作为后缀
import os
import sys

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

# class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
#     id = db.Column(db.Integer, primary_key=True)  # 主键
#     name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

# (env) $ flask shell
# >>> from app import db
# >>> db.create_all()

# >>> db.drop_all()
# >>> db.create_all()
import click

@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
# (env) $ flask initdb
# (env) $ flask initdb --drop

# 向数据库中添加记录
# >>> from app import User, Movie  # 导入模型类
# >>> user = User(name='Grey Li')  # 创建一个 User 记录
# >>> m1 = Movie(title='Leon', year='1994')  # 创建一个 Movie 记录
# >>> m2 = Movie(title='Mahjong', year='1996')  # 再创建一个 Movie 记录
# >>> db.session.add(user)  # 把新创建的记录添加到数据库会话
# >>> db.session.add(m1)
# >>> db.session.add(m2)
# >>> db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
# 没有传入 id 字段（主键），因为 SQLAlchemy 会自动处理这个字段

# 读取与查询
# >>> from app import Movie  # 导入模型类
# >>> movie = Movie.query.first()  # 获取 Movie 模型的第一个记录（返回模型类实例）
# >>> movie.title  # 对返回的模型类实例调用属性即可获取记录的各字段数据
# 'Leon'
# >>> movie.year
# '1994'
# >>> Movie.query.all()  # 获取 Movie 模型的所有记录，返回包含多个模型类实例的列表
# [<Movie 1>, <Movie 2>]
# >>> Movie.query.count()  # 获取 Movie 模型所有记录的数量
# 2
# >>> Movie.query.get(1)  # 获取主键值为 1 的记录
# <Movie 1>
# >>> Movie.query.filter_by(title='Mahjong').first()  # 获取 title 字段值为 Mahjong 的记录
# <Movie 2>
# >>> Movie.query.filter(Movie.title=='Mahjong').first()  # 等同于上面的查询，但使用不同的过滤方法
# <Movie 2>
# 表的实际名称是模型类的小写形式（自动生成），如果你想自己指定表名，可以定义 __tablename__ 属性

# 更新
# >>> movie = Movie.query.get(2)
# >>> movie.title = 'WALL-E'  # 直接对实例属性赋予新的值即可
# >>> movie.year = '2008'
# >>> db.session.commit()  # 注意仍然需要调用这一行来提交改动

# 删除
# >>> movie = Movie.query.get(1)
# >>> db.session.delete(movie)  # 使用 db.session.delete() 方法删除记录，传入模型实例
# >>> db.session.commit()  # 提交改动
from flask import render_template
# 程序内修改
# @app.route('/')
# def index():
#     user = User.query.first()  # 读取用户记录
#     movies = Movie.query.all()  # 读取所有电影记录
#     return render_template('index.html', user=user, movies=movies)

import click

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    
    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done.')

# chapter 6 Template2 https://github.com/greyli/flask-tutorial/blob/master/chapters/c6-template2.md

@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('4046.html'), 404

# @app.route('/')
# def index6():
#     movies = Movie.query.all()
#     return render_template('index6.html', movies=movies)

# 基模板中需要在实际的子模板中追加或重写的部分则可以定义成块（block）。
# 块使用 block 标签创建， {% block 块名称 %} 作为开始标记，{% endblock %} 或 {% endblock 块名称 %} 作为结束标记
# 默认的块重写行为是覆盖，如果你想向父块里追加内容，可以在子块中使用 super() 声明，即 {{ super() }}

# 添加了一个新的 <meta> 元素，这个元素会设置页面的视口，让页面根据设备的宽度来自动缩放页面
# 让移动设备拥有更好的浏览体验; 添加了一个导航栏

# chapter 7 Form https://github.com/greyli/flask-tutorial/blob/master/chapters/c7-form.md
# 在 <form> 标签里使用 method 属性将提交表单数据的 HTTP 请求方法指定为 POST。如果不指定，则会默认使用 GET 方法，
# 这会将表单数据通过 URL 提交，容易导致数据泄露，而且不适用于包含大量数据的情况。
# <input> 元素必须要指定 name 属性，否则无法提交数据，
# 在服务器端，我们也需要通过这个 name 属性值来获取对应字段的数据
# <label> 元素不是必须的，只是为了辅助鼠标用户。当使用鼠标点击标签文字时，会自动激活对应的输入框，这对复选框来说比较有用。
# for 属性填入要绑定的 <input> 元素的 id 属性值。
from flask import request, url_for, redirect, flash
from flask_login import current_user, login_required
@app.route('/', methods=['GET', 'POST'])
def index7():
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index7'))  # 重定向到主页
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index7'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index7'))  # 重定向回主页

    movies = Movie.query.all()
    return render_template('index7.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

# chapter 8 Login https://github.com/greyli/flask-tutorial/blob/master/chapters/c8-login.md
# Flask 的依赖 Werkzeug 内置了用于生成和验证密码散列值的函数，werkzeug.security.generate_password_hash() 用来为给定的密码生成密码散列值，
# 而 werkzeug.security.check_password_hash() 则用来检查给定的散列值和密码是否对应
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值
# 模型（表结构）发生变化，我们需要重新生成数据库（这会清空数据）

import click

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()  # assume the first one as admin
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')

from flask_login import LoginManager

login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象
from flask_login import UserMixin, login_user
# class User(db.Model, UserMixin): is_authenticated 属性：
# 如果当前用户已经登录，那么 current_user.is_authenticated 会返回 True， 否则返回 False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        
        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index7'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面
    
    return render_template('login.html')

from flask_login import login_required, logout_user

@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index7'))  # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        
        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index7'))
    
    return render_template('settings.html')






