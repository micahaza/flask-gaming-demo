from . import db
from sqlalchemy.ext.hybrid import hybrid_property
from flask import current_app

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    real_money_wallet = db.relationship('RealMoneyWallet', uselist=False, backref='user')
    bonus_money_wallets = db.relationship('BonusMoneyWallet', uselist=True)
    bets = db.relationship('Bet', uselist=True)
    wins = db.relationship('Win', uselist=True)
    
    @hybrid_property
    def bonus_money_sum(self):
        return sum(bm.balance for bm in self.bonus_money_wallets)

    def __init__(self, username=None, email=None, password_hash=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '<User({}) {} >'.format(str(self.id), self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

class RealMoneyWallet(db.Model):

    __tablename__ = 'real_money_wallets'
    
    def __init__(self, balance=None):
        self.balance = balance
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    balance = db.Column(db.Float, default = 0)

    def __repr__(self):
        return '<RealMoneyWallet {}>'.format(self.balance)

class BonusMoneyWallet(db.Model):

    __tablename__ = 'bonus_money_wallets'

    def __init__(self, balance=None):
        self.initial_balance = balance
        self.balance = balance
    
    @hybrid_property
    def cash_in_possible(self):
        return self.initial_balance * current_app.config['WAGERING_REQUIREMENT'] <= sum(b.amount for b in self.bets)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    initial_balance = db.Column(db.Float, default = 0)
    balance = db.Column(db.Float, default = 0)
    depleted = db.Column(db.Boolean, default = False)
    bets = db.relationship('Bet', uselist=True)
    
    def __repr__(self):
        return '<BonusMoneyWallet {}>'.format(self.balance)

class Bet(db.Model):
    
    __tablename__ = 'bets'

    def __init__(self, amount, amount_type='real', bonus_money_wallet_id = None):
        self.amount = amount
        self.amount_type = amount_type
        self.bonus_money_wallet_id = bonus_money_wallet_id

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bonus_money_wallet_id = db.Column(db.Integer, db.ForeignKey('bonus_money_wallets.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False, default = 0)
    amount_type = db.Column(db.Enum('real', 'bonus'), nullable=False, server_default=("real"))
    
class Win(db.Model):
    
    __tablename__ = 'wins'

    def __init__(self, amount, amount_type='real', bonus_money_wallet_id = None):
        self.amount = amount
        self.amount_type = amount_type
        self.bonus_money_wallet_id = bonus_money_wallet_id

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bonus_money_wallet_id = db.Column(db.Integer, db.ForeignKey('bonus_money_wallets.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False, default = 0)
    amount_type = db.Column(db.Enum('real', 'bonus'), nullable=False, server_default=("real"))