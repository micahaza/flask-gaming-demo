from . import db

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    real_money = db.relationship('RealMoney', uselist=False, backref='user')
    bonus_moneys = db.relationship('BonusMoney', uselist=True)
    bets = db.relationship('Bet', uselist=True)
    wins = db.relationship('Win', uselist=True)
    
    def __init__(self, username=None, email=None, password_hash=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '<User({}) {} >'.format(str(self.id), self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

class RealMoney(db.Model):

    __tablename__ = 'real_moneys'
    
    def __init__(self, balance=None):
        self.balance = balance
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    balance = db.Column(db.Float, default = 0)

    def __repr__(self):
        return '<RealMoney {}>'.format(self.balance)

class BonusMoney(db.Model):

    __tablename__ = 'bonus_moneys'

    def __init__(self, balance=None):
        self.balance = balance
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Float, default = 0)

    def __repr__(self):
        return '<BonusMoney {}>'.format(self.balance)
    
class Bet(db.Model):
    
    __tablename__ = 'bets'

    def __init__(self, amount):
        self.amount = amount

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default = 0)
    
class Win(db.Model):
    
    __tablename__ = 'wins'

    def __init__(self, amount):
        self.amount = amount

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default = 0)