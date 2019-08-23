from flask_gaming.models import User, Bet, Win
import random


class NotEnoughMoneyException(Exception):
    def __init__(self, message):
        self.message = message

class BaseSpinner(object):
    
    def __init__(self, config, user):
        self.config = config
        self.user = user

    def random_win(self):
        # RNG magic :)
        return random.choice([0, 0, 1]) * 4

class RealMoneySpinner(BaseSpinner):
    
    def __init__(self, config, user):
        super(RealMoneySpinner, self).__init__(config, user)
    
    def spin(self):
        win_amount = self.random_win()
        bet = Bet(self.config['BET_AMOUNT'], amount_type='real')
        win = Win(win_amount, amount_type='real')
        self.user.real_money.balance -= self.config['BET_AMOUNT']
        self.user.bets.append(bet)
        self.user.wins.append(win)
        self.user.real_money.balance += win_amount
        self.user.save()

class BonusMoneySpinner(BaseSpinner):
    
    def __init__(self, config, user):
        super(BonusMoneySpinner, self).__init__(config, user)
    
    def spin(self):
        win_amount = self.random_win()
        for bw in self.user.bonus_moneys:
            if bw.balance >= self.config['BET_AMOUNT']:
                bw.balance -= self.config['BET_AMOUNT']
                bet = Bet(self.config['BET_AMOUNT'], amount_type='bonus', bonus_money_wallet_id = bw.id)
                win = Win(win_amount, amount_type='bonus', bonus_money_wallet_id = bw.id)
                if win_amount > 0:
                    bw.balance += win_amount
                self.user.bets.append(bet)
                self.user.wins.append(win)
                if bw.cash_in_possible:
                    # convert bonus money to real money and transfer it to player
                    self.user.real_money.balance += bw.balance
                    # clean up this bonus wallet
                    bw.balance = 0
        self.user.save()

class GamePlay(object):

    def __init__(self, config, user):
        self.config = config
        self.user = user
        self.real_money_spinner = RealMoneySpinner(config, user)
        self.bonus_money_spinner = BonusMoneySpinner(config, user)

    def get_spinner(self):
        if self.user.real_money is not None and self.user.real_money.balance >= self.config['BET_AMOUNT']:
            return self.real_money_spinner
        elif self.user.bonus_money_sum >= self.config['BET_AMOUNT']:
            return self.bonus_money_spinner
        else:
            raise NotEnoughMoneyException("User has not enough money to play")

    def spin(self):
        spinner = self.get_spinner()
        spinner.spin()
