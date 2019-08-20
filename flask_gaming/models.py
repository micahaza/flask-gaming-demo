from . import db

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    wallet = db.relationship('Wallet', backref='user')

    def __init__(self, username=None, email=None, password_hash=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def real_money_balance(self):
        return 0
        
    def bonus_money_balance(self):
        return 0
        
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Wallet(db.Model):

    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_real_money_wallet = db.Column(db.Boolean, default=False)

class WalletHistory(db.Model):

    __tablename__ = 'wallet_histories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default = 0)
    
class Bet(db.Model):
    
    __tablename__ = 'bets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default = 0)
    
class Win(db.Model):
    
    __tablename__ = 'wins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default = 0)