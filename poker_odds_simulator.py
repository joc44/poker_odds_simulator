from random import choice


class Suit:
    def __init__(self, suit: str):
        self.suit = suit

    def __str__(self):
        return self.suit


class Kind:
    value = {'2': 2,
             '3': 3,
             '4': 4,
             '5': 5,
             '6': 6,
             '7': 7,
             '8': 8,
             '9': 9,
             '0': 10,
             'J': 11,
             'Q': 12,
             'K': 13,
             'A': 14
             }

    def __init__(self, kind: str):
        self.kind = kind

    def __str__(self):
        return self.kind


class Card:
    def __init__(self, suit: Suit, kind: Kind):
        self.suit = suit
        self.kind = kind

    def __str__(self):
        return str(self.suit) + str(self.kind)


class Deck:
    def __init__(self):
        self.deck = []
        for suit in [Suit('C'), Suit('D'), Suit('H'), Suit('S')]:
            for kind in [Kind('A'), Kind('2'), Kind('3'), Kind('4'), Kind('5'), Kind('6'), Kind('7'), Kind('8'),
                         Kind('9'), Kind('0'), Kind('J'), Kind('Q'), Kind('K')]:
                self.deck.append(Card(suit, kind))

    def __str__(self):
        text = ''
        for card in self.deck:
            text += str(card)
        return text

    def deal(self, card: str):
        if card == '??':
            return Card(Suit('?'), Kind('?'))
        for deck_card in self.deck:
            if str(deck_card) == str(Card(Suit(card[0]), Kind(card[1]))):
                _temp = deck_card
                self.deck.remove(deck_card)
                return _temp
        print('Missdealing. Bye!')
        exit()

    def random_deal(self):
        _temp = choice(self.deck)
        self.deck.remove(_temp)
        return _temp


class Common:
    def __init__(self, cards: list):
        self.cards = cards

    def __str__(self):
        text = ''
        for card in self.cards:
            text += str(card) + ' '
        return text


class Hand:
    def __init__(self, cards: list):
        self.cards = cards

    def __str__(self):
        text = ''
        for card in self.cards:
            text += str(card) + ' '
        return text


class Table:
    def deal(self, deck: Deck, common: Common, player: Hand, others: list):
        self.deck = deck
        self.common = common
        self.player = player
        self.others = others

    def show_table(self):
        print('TABLE:')
        print('Deck:', self.deck)
        print('Common cards:', self.common)
        print("Player's hand: ", self.player)
        print("Other's hand:")
        for i, hand in enumerate(self.others):
            print(str(i + 2) + '.player:', str(hand))
        print()

class Simulation:
    def __init__(self, table: Table):
        self.table = table

    def complete(self):
        for i, card in enumerate(self.table.common.cards):
            if str(card) == '??':
                self.table.common.cards[i] = deck.random_deal()

        for i, card in enumerate(self.table.player.cards):
            if str(card) == '??':
                self.table.player.cards[i] = deck.random_deal()

        for i, hand in enumerate(self.table.others):
            for k, card in enumerate(hand.cards):
                if str(card) == '??':
                    self.table.others[i].cards[k] = deck.random_deal()

        self.table.show_table()

    def evalution(self):
        pass

    def simulation(self):
        self.complete()

        player_value = self.evalution(self.table.common.cards[:] + self.table.player.cards[:])

        others_value = []
        for i, opponent in enumerate(self.table.others):
            others_value.append(self.evalution(self.table.common.cards[:] + opponent.cards[:]))





if __name__ == '__main__':
    print('\ >>> START PROGRAM\n')

    N = 1
    win = 0
    lose = 0
    split = 0

    for i in range(N):
        deck = Deck()
        player = Hand([deck.deal('HA'), deck.deal('D9')])
        othes = [Hand([deck.deal('??'), deck.deal('??')]),
                 Hand([deck.deal('??'), deck.deal('??')]),
                 Hand([deck.deal('??'), deck.deal('??')]),
                 Hand([deck.deal('??'), deck.deal('??')]),
                 Hand([deck.deal('??'), deck.deal('??')]
                      )]
        common = Common([deck.deal('HK'),
                         deck.deal('D4'),
                         deck.deal('C8'),
                         deck.deal('CA'),
                         deck.deal('SJ')
                         ])

        table = Table()
        table.deal(deck, common, player, othes)
        #table.show_table()

        simulation = Simulation(table)
        #simulation.complete()

        result = simulation.simulation()
        if result == True:
            win +=1
        elif result == False:
            lose += 1
        else:
            split += 1

    print('Win:\t', round(win / N * 100, 2), ' %')
    print('Lose:\t', round(lose / N * 100, 2), ' %')
    print('Split:\t', round(split / N * 100, 2), ' %')
    print()
