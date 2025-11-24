from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from login_manager import login_manager
from controllers import setup_routes

app = Flask(__name__)


# DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/chainsawman'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'


# Flask_Login 설정
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'  # 로그인 페이지의 뷰 함수 이름

setup_routes(app)   # 라우팅 설정

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run()