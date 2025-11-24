from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# -----------------------------
# Team 테이블
# -----------------------------
class Team(db.Model):
    __tablename__ = 'team'
    __table_args__ = {'extend_existing': True}  # 기존 테이블 참조
    team_id = db.Column(db.BigInteger, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)

    humans = db.relationship('Human', backref='team', lazy=True)
    missions = db.relationship('Mission', backref='team', lazy=True)


# -----------------------------
# Human 테이블
# -----------------------------
class Human(db.Model, UserMixin):
    __tablename__ = 'human'
    __table_args__ = {'extend_existing': True}
    human_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum('ACTIVE','INACTIVE','RETIRED','DEAD'), default='ACTIVE')
    team_id = db.Column(db.BigInteger, db.ForeignKey('team.team_id'))

    contracts = db.relationship('Contract', backref='human', lazy=True)
    bounty_claims = db.relationship('BountyClaim', backref='human', lazy=True)
    account = db.relationship('Account', backref='human', uselist=False)

        # Flask-Login이 세션 관리할 때 필요한 ID 반환
    def get_id(self):
        return str(self.human_id)



# -----------------------------
# Demon 테이블
# -----------------------------
class Demon(db.Model):
    __tablename__ = 'demon'
    __table_args__ = {'extend_existing': True}
    demon_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Enum('C','B','A','S','SS'), nullable=False)
    bounty = db.Column(db.Integer, nullable=False)
    civilian_killed_total = db.Column(db.Integer, default=0)
    civilian_injured_total = db.Column(db.Integer, default=0)

    contracts = db.relationship('Contract', backref='demon', lazy=True)
    bounty_claims = db.relationship('BountyClaim', backref='demon', lazy=True)
    battles = db.relationship('Battle', backref='demon', lazy=True)


# -----------------------------
# Contract 테이블
# -----------------------------
class Contract(db.Model):
    __tablename__ = 'contract'
    __table_args__ = {'extend_existing': True}
    contract_id = db.Column(db.Integer, primary_key=True)
    human_id = db.Column(db.Integer, db.ForeignKey('human.human_id'), nullable=False)
    demon_id = db.Column(db.Integer, db.ForeignKey('demon.demon_id'), nullable=False)
    cost_type = db.Column(db.Enum('LIFE','MEMORY','EMOTION','OTHER'), nullable=False)
    cost_desc = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('ACTIVE','BROKEN','EXPIRED'), default='ACTIVE')


# -----------------------------
# Mission 테이블
# -----------------------------
class Mission(db.Model):
    __tablename__ = 'mission'
    __table_args__ = {'extend_existing': True}
    mission_id = db.Column(db.BigInteger, primary_key=True)
    team_id = db.Column(db.BigInteger, db.ForeignKey('team.team_id'), nullable=False)
    objective = db.Column(db.String(255), nullable=False)
    target_desc = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('PLANNED','IN_PROGRESS','SUCCESS','FAIL'), default='PLANNED')
    created_at = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)

    battles = db.relationship('Battle', backref='mission', lazy=True)


# -----------------------------
# Battle 테이블
# -----------------------------
class Battle(db.Model):
    __tablename__ = 'battle'
    __table_args__ = {'extend_existing': True}
    battle_id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.BigInteger, db.ForeignKey('mission.mission_id'), nullable=True)
    demon_id = db.Column(db.Integer, db.ForeignKey('demon.demon_id'), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False)
    ended_at = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(150), nullable=False)
    outcome = db.Column(db.Enum('HUMAN_WIN','DEMON_WIN','DRAW','ESCAPE'), nullable=False)
    civilian_killed = db.Column(db.Integer, default=0)
    civilian_injured = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=True)

    bounty_claims = db.relationship('BountyClaim', backref='battle', lazy=True)


# -----------------------------
# BountyClaim 테이블
# -----------------------------
class BountyClaim(db.Model):
    __tablename__ = 'bountyclaim'
    __table_args__ = {'extend_existing': True}
    claim_id = db.Column(db.Integer, primary_key=True)
    battle_id = db.Column(db.Integer, db.ForeignKey('battle.battle_id'), nullable=False)
    demon_id = db.Column(db.Integer, db.ForeignKey('demon.demon_id'), nullable=False)
    human_id = db.Column(db.Integer, db.ForeignKey('human.human_id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    claim_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(255), nullable=True)


# -----------------------------
# Account 테이블
# -----------------------------
class Account(db.Model):
    __tablename__ = 'account'
    __table_args__ = {'extend_existing': True}
    account_id = db.Column(db.Integer, primary_key=True)
    hunter_id = db.Column(db.Integer, db.ForeignKey('human.human_id'), nullable=False)
    balance = db.Column(db.Integer, default=0)
    total_income = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Integer, default=0)
    last_tx_type = db.Column(db.Enum('IN','OUT'), nullable=True)
    last_tx_amount = db.Column(db.Integer, nullable=True)
    last_tx_desc = db.Column(db.String(255), nullable=True)
    history = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False)
