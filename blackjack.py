import sys
import time
import os
import dearpygui.dearpygui as dpg

class Deck:
    def __init__(self):
        import random
        self.cards_pos = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = []
        a = 52
        for x in range(a):
            choice = random.randint(0, 12)
            if self.cards_pos[choice] in self.cards:
                while self.cards.count(self.cards_pos[choice]) > 4:
                    choice = random.randint(0, 12)
                self.cards.append(self.cards_pos[choice])
            else:
                self.cards.append(self.cards_pos[choice])

    def remove_card(self):
        draw = self.cards[len(self.cards) - 1]
        self.cards.pop(len(self.cards) - 1)
        return draw


class Player:
    def __init__(self, deck):
        self.bust = False
        self.hand = []
        self.blackjack = False
        self.hand.append(deck.remove_card())
        self.hand.append(deck.remove_card())
        print('Your total: ', end='')
        for i in self.hand:
            print(f' [{i}]', end='')
        print()
        self.calculate(dis=True)

    def draw_card(self, deck):
        self.hand.append(deck.remove_card())
        print('You have:', end='')
        for i in self.hand:
            print(f' [{i}]', end='')
        print()
        total = self.calculate(dis=False)[0]

    def calculate(self, dis):
        total = 0
        total_a = 0
        letter_cards = {'J': 10, 'Q': 10, 'K': 10}

        for i in self.hand:
            try:
                i = int(i)
                total += i
                total_a += i
            except ValueError:
                if i in letter_cards:
                    total += letter_cards[i]
                    total_a += letter_cards[i]
                else:
                    total_a += 11
                    total += 1
        if dis:
            if total == total_a or total_a > 21:
                print('Your total:', total)
            else:
                print('Your total:', total, 'or', total_a)

            if total > 21:
                print("You're bust!")
                self.bust = True
        else:
            if total > 21:
                self.bust = True
            return total, total_a, self.blackjack, self.bust


class Bot:
    def __init__(self, deck):
        self.bust = False
        self.blackjack = False
        self.stand = False
        self.drawn = False
        self.hand = []
        self.hand.append(Deck.remove_card(deck))
        self.hand.append(Deck.remove_card(deck))

    def display_cards(self, rev):
        if rev:
            print('Computer Has: ', end='')
            for i in self.hand:
                print(f' [{i}]', end='')
            print()
        else:
            print('Computer Has: [?]', f'[{self.hand[1]}] ')

    def bot_calc(self, dis):
        total, total_a, self.blackjack, self.bust = Player.calculate(self=self, dis=dis)
        return total, total_a, self.blackjack, self.bust

    def bot_plays(self, deck):
        import time
        total, total_a, self.blackjack, self.bust = self.bot_calc(dis=False)

        if not self.drawn:
            self.display_cards(rev=True)
            self.drawn = True

        if self.blackjack or self.bust or self.stand:
            return self.blackjack, self.bust
        elif total == 21 or total_a == 21:
            self.blackjack = True
        elif total > 21 and total_a > 21:
            self.bust = True

        if total <= total_a < 15:
            print('Computer Draws')
            self.hand.append(Deck.remove_card(deck))
            self.display_cards(rev=True)
            time.sleep(0.5)
            total, total_a, self.blackjack, self.bust = self.bot_calc(dis=False)
            self.drawn = True
        else:
            self.stand = True
            print("Computer Stands")

        self.bot_plays(deck)


class Main:
    def __init__(self, p_money):
        self.money = p_money
        self.bet = 0
        while True:
            try:
                self.bet = int(input('You have $' + '{:,}'.format(self.money) + ', place a bet here: '))
                if self.bet <= self.money:
                    break
                else:
                    int('')
            except ValueError:
                print("Please input a valid number")

        self.games = 0
        self.winner = None  # 0 if player, 1 if computer
        self.__dict__[f'deck{self.games}'] = Deck()
        self.bot = Bot(deck=self.__dict__[f'deck{self.games}'])
        self.bot.display_cards(rev=False)
        self.player = Player(deck=self.__dict__[f'deck{self.games}'])

    def run(self):
        inp = input('type d to draw, type s to stand: ')
        if 'd' in inp:
            self.bot.display_cards(rev=False)
            self.player.draw_card(self.__dict__[f'deck{self.games}'])
            self.player.calculate(dis=True)
            x, y, z, a = self.player.calculate(dis=False)
            if z:
                self.winner = 0
            if a:
                self.winner = 1
        if 's' in inp:
            if self.player.calculate(dis=False)[0] == 21 or self.player.calculate(dis=False)[1] == 21:
                self.winner = 0
            else:
                self.bot.bot_plays(self.__dict__[f'deck{self.games}'])
                c, d = self.bot.bot_plays(self.__dict__[f'deck{self.games}'])
                if c:
                    self.winner = 1
                elif d:
                    self.winner = 0
                else:
                    p_tot, p_tot_a = self.player.calculate(dis=False)[0], self.player.calculate(dis=False)[1]
                    b_tot, b_tot_a = self.bot.bot_calc(dis=False)[0], self.bot.bot_calc(dis=False)[1]
                    if 21 >= p_tot > b_tot or 21 >= p_tot_a > b_tot:
                        self.winner = 0
                    elif 21 >= b_tot > p_tot or 21 >= b_tot_a > p_tot:
                        self.winner = 1
                    elif 21 > p_tot == b_tot or 21 > p_tot == b_tot_a or 21 > b_tot > p_tot or 21 > b_tot == p_tot_a:
                        self.winner = 2
        if self.winner == 1:
            print("computer wins")
            self.money -= self.bet
        elif self.winner == 0:
            print("Player wins")
            self.money += self.bet
        elif self.winner == 2:
            print("Oooh its a tie, see, no one cares")
        return self.winner, self.money

    def new_deck(self, rem):
        self.games += 1
        self.__dict__[f'deck{self.games}'] = Deck()
        if rem:
            self.__dict__[f'deck{self.games}'].remove_card()


money = ''
try:
    f = open('ALLOWED TO ENTER.txt', 'x')
    if os.stat('ALLOWED TO ENTER.txt').st_size == 0:
        f.write('Player is allowed to freely enjoy the casino\n')
        f.write('Player money = 1000')
        money = int(money + '1000')
        loan = False
except FileExistsError:
    with open('ALLOWED TO ENTER.txt', 'r') as f:
        for line in f:
            if 'Player money' in line:
                l = list(line)
                for i in l:
                    try:
                        int(i)
                        money = money + i
                    except ValueError:
                        pass
            if 'On a loan' in line:
                loan = True
            else: loan = False
        money = int(''.join(money))
        if money > 50000 and loan:
            money -= 50000
            print("As per your loan, we subtracted 50,000")
            loan = False
            open('ALLOWED TO ENTER.txt', 'w').writelines(['Player is allowed to freely enjoy the casino\n',
                                                          f'Player money = {money}'])

with open('ALLOWED TO ENTER.txt', 'r') as f:
    if 'BANNED FOR LIFE' not in f.read():
        main = Main(p_money=money)

        while True:
            winner, money = main.run()
            if winner is not None:
                if money > 0:
                    ans = input('\nPlay again? y/n ')
                    if 'y' in ans:
                        main = Main(p_money=money)
                    elif loan:
                        print("Don't forget about that loan")
                        open('ALLOWED TO ENTER.txt', 'w').writelines(['Player is allowed to freely enjoy the casino\n',
                                                                      f'Player money = {money}', '\nOn a loan'])
                        sys.exit()
                    else:
                        print('K, i didnt even wanna play anyways\nTotal money: $' + '{:,}'.format(money))
                        open('ALLOWED TO ENTER.txt', 'w').writelines(['Player is allowed to freely enjoy the casino\n',
                                                                      f'Player money = {money}'])
                        sys.exit()
                elif not loan:
                    time.sleep(2)
                    print("Ooooooh baby, you're all out of cash")
                    time.sleep(2)
                    print("I can help you out a bit, with a loan")
                    time.sleep(2)
                    print("Does that sound good?")
                    time.sleep(1)
                    print("I'm kidding, you don't have a choice")
                    time.sleep(1)
                    loan = True
                    money += 50000
                    open('ALLOWED TO ENTER.txt', 'w').writelines(['Player is allowed to freely enjoy the casino\n',
                                                                  f'Player money = {money}', '\nOn a loan'])
                    inpu = input('\nPlay again? y/n ')
                    if 'y' in inpu:
                        main = Main(p_money=money)
                    else:
                        print("Don't forget about that loan")
                        sys.exit()
                elif loan:
                    time.sleep(2)
                    print("You dumb ass, you lost all of my money! You're gonna pay, you're gonna pay big time!")
                    time.sleep(2)
                    for i in range(100):
                        print('Total money: ' + str(-1 * (i ** 10)))
                        time.sleep(0.05)
                    with open('ALLOWED TO ENTER.txt', 'w') as f:
                        f.writelines(['BANNED FOR LIFE', 'Player money = - 1 billion million'])
                    sys.exit()
    else:
        print("HEY! You're never allowed back into my casino! Ya hear me?\nNEVER!")
        sys.exit()
