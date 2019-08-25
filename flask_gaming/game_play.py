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
        self.user.real_money_wallet.balance -= self.config['BET_AMOUNT']
        self.user.bets.append(bet)
        self.user.wins.append(win)
        self.user.real_money_wallet.balance += win_amount
        self.user.save()

class BonusMoneySpinner(BaseSpinner):
    
    def __init__(self, config, user):
        super(BonusMoneySpinner, self).__init__(config, user)
    
    def mark_depleted_wallets(self):
        for bw in (bw for bw in self.user.bonus_money_wallets if bw.depleted == False):
            if bw.balance <= self.config['BET_AMOUNT']:
                bw.depleted = True
        self.user.save()

    def bonus_money_convert(self):
        pass

    def spin(self):

        self.mark_depleted_wallets()
        win_amount = self.random_win()
        for bw in (bw for bw in self.user.bonus_money_wallets if bw.depleted == False):
            bw.balance -= self.config['BET_AMOUNT']
            bet = Bet(self.config['BET_AMOUNT'], amount_type='bonus', bonus_money_wallet_id = bw.id)
            win = Win(win_amount, amount_type='bonus', bonus_money_wallet_id = bw.id)
            if win_amount > 0:
                bw.balance += win_amount
            self.user.bets.append(bet)
            self.user.wins.append(win)
            if bw.cash_in_possible:
                # convert bonus money to real money and transfer it to player
                self.user.real_money_wallet.balance += bw.balance
                # clean up this bonus wallet
                bw.balance = 0
                bw.depleted = True
            break;
        self.user.save()

class GamePlay(object):

    def __init__(self, config, user):
        self.config = config
        self.user = user
        self.real_money_wallet_spinner = RealMoneySpinner(config, user)
        self.bonus_money_spinner = BonusMoneySpinner(config, user)

    def get_spinner(self):
        if self.user.real_money_wallet is not None and self.user.real_money_wallet.balance >= self.config['BET_AMOUNT']:
            return self.real_money_wallet_spinner
        elif self.user.bonus_money_sum >= self.config['BET_AMOUNT']:
            return self.bonus_money_spinner
        else:
            raise NotEnoughMoneyException("User has not enough money to play")

    def spin(self):
        spinner = self.get_spinner()
        spinner.spin()
