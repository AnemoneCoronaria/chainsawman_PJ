from flask import render_template, request, jsonify, abort, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Account, Battle, BountyClaim, Contract, Demon, Human, Mission, Team
from login_manager import login_manager
from sqlalchemy import func

def setup_routes(app):
    
    @login_manager.user_loader
    def load_human(human_id):
        return Human.query.get(int(human_id))
    # 로그인 후 Flask-Login이 세션에 저장한 human_id를 가져와
    # db에서 Human 객체를 조회 후 조회한 객체를 current_user로 설정


    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/mainpage')
    def mainpage():
        human_count = Human.query.count()
        demon_count = Demon.query.count()

        # 팀별 인간수 집계
        team_stats = (
            db.session.query(
                Team.team_name, 
                func.count(Human.human_id)).join(Human, Team.team_id == Human.human_id).group_by(Team.team_id).all()
        )

        return render_template(
            'mainpage.html', 
            human_count=human_count, 
            demon_count=demon_count,
            team_stats=team_stats
        )
    


