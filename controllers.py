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
                func.count(Human.human_id)).join(Human, Team.team_id == Human.team_id).group_by(Team.team_id).all()
        )

        return render_template(
            'mainpage.html', 
            human_count=human_count, 
            demon_count=demon_count,
            team_stats=team_stats,
            current_user=current_user
        )
    
    # @app.route('/hunter/<int:human_id>')
    # def hunter_detail(human_id):
    #     hunter = Human.query.get_or_404(human_id)
    #     battles = Battle.query.join(Mission).filter(Battle.demon_id.in_(
    #         [c.demon_id for c in hunter.contracts]
    #     )).all()
    #     return render_template('hunter_detail.html', hunter=hunter, battles=battles)

    @app.route('/hunter/<int:human_id>')
    def hunter_detail(human_id):
        hunter = Human.query.get_or_404(human_id)

        # 헌터가 속한 팀의 전투 기록 가져오기
        battles = Battle.query.join(Mission).filter(Mission.team_id == hunter.team_id).all()

        # 헌터가 직접 청구한 현상금 기록
        claims = BountyClaim.query.filter_by(human_id=human_id).all()

        return render_template('hunter_detail.html', hunter=hunter, battles=battles, claims=claims)
    


    @app.route('/login', methods=['POST'])
    def login():
        username = request.form.get('username')
        hunter = Human.query.filter_by(name=username).first()
        if hunter:
            login_user(hunter)  # Flask-Login 세션에 저장
            return redirect(url_for('mainpage'))
        else:
            return jsonify({'error': '존재하지 않는 헌터입니다'}), 400


    @app.route('/signup', methods=['POST'])
    def signup():
        humanname = request.form.get('humanname')
        teamid = request.form.get('teamid')

        new_human = Human(name=humanname, status='ACTIVE', team_id=teamid)
        db.session.add(new_human)
        db.session.commit()

        return jsonify({'message': f'{humanname} 헌터가 팀 {teamid}에 가입되었습니다!'})

