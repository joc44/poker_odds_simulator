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

    def value(self, card: str):
        return Kind.value[card[1]]


    def evalution(self, cards):
        value_from_seven = {'rank': 0, 'kind': 0, 'kicker': [], '_set':[]}
        seven_cards = set()
        for card in cards:
            seven_cards.add(str(card))

        # Royal_Flush
        for suit in ['C', 'D', 'H', 'S']:
            _set = set()
            for kind in ['A', '0', 'J', 'Q', 'K']:
                _set.add(suit + kind)
            if _set.issubset(seven_cards):
                value_from_seven['rank'] = 9
                value_from_seven['_set'] = _set
                return value_from_seven

        # Straight_Flush
        for suit in ['C', 'D', 'H', 'S']:
            _set = []
            for kind in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K']:
                if (suit+kind) in seven_cards:
                    _set.append(suit+kind)
                elif len(_set) < 5:
                    _set = []

            if len(_set) > 4:
                _set = _set[-5:]
                value_from_seven['rank'] = 8
                value_from_seven['kind'] = self.value(_set[-1])
                value_from_seven['_set'] = _set
                return value_from_seven


        # típus_számoló
        k_counter = {}
        for card in seven_cards:
            if card[1] in k_counter.keys():
                k_counter[card[1]] += 1
            else:
                k_counter[card[1]] = 1


        # Four_of_a_Kind

        for kind in k_counter.items():
            if kind[1] == 4:
                _set = []
                for card in seven_cards:
                    if card[1] == kind[0]:
                        _set.append(card)
                value_from_seven['rank'] = 7
                value_from_seven['kind'] = self.value(_set[0])
                value_from_seven['kicker'] = [self.value(sorted(seven_cards.difference(_set), key=self.value)[-1])]
                value_from_seven['_set'] = _set
                return value_from_seven

        # Full_House
        value = 0
        for kind in k_counter.items():
            if kind[1] == 3:
                if Kind.value[kind[0]] > value:
                    value = Kind.value[kind[0]]
                    _set = []
                    for card in seven_cards:
                        if card[1] == kind[0]:
                            _set.append(card)
                    value_from_seven['rank'] = 3
                    value_from_seven['kind'] = self.value(_set[0])*3
                    value_from_seven['kicker'] = [self.value(sorted(seven_cards.difference(_set), key=self.value)[-1])], [self.value(sorted(seven_cards.difference(_set), key=self.value)[-2])]
                    value_from_seven['_set'] = _set

        if value_from_seven['rank'] == 3:
            _value_from_seven = value_from_seven['kind']
            k_counter2 = k_counter.copy()
            k_counter2.pop(_set[0][1])
            value = 0
            for kind in k_counter2.items():
                if kind[1] == 3 or kind[1] == 2:
                    if Kind.value[kind[0]] > value:
                        _set2 = []
                        for card in seven_cards:
                            if card[1] == kind[0]:
                                _set2.append(card)
                        _set2 = _set2[:2]
                        value_from_seven['rank'] = 6
                        value_from_seven['kind'] = self.value(_set2[0]) * 2 + -_value_from_seven
                        value_from_seven['kicker'] = []
                        value_from_seven['_set'] = _set + _set2

        # szín_számoló
        s_counter = {}
        for card in seven_cards:
            if card[0] in s_counter.keys():
                s_counter[card[0]] += 1
            else:
                s_counter[card[0]] = 1

        # Flush
        for suit in s_counter.items():
            if suit[1] > 4:
                _set = []
                for card in seven_cards:
                    _set.append(card)
                _set = sorted(_set, key=self.value)[-5:]
                value_from_seven['rank'] = 5
                value_from_seven['kind'] = self.value(_set[-1])
                value_from_seven['kicker'] = []
                value_from_seven['_set'] = _set
                return value_from_seven

        # Straight

        _set = []
        for kind in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K']:
            for card in seven_cards:
                if kind == card[1]:
                    _set.append(card)
                    break
            if _set:
                if _set[-1][1] != kind and len(_set) < 5:
                    _set = []
                elif _set[-1][1] != kind and len(_set) >4:
                    break
        if len(_set) > 4:
            _set = _set[-5:]
            value_from_seven['rank'] = 4
            value_from_seven['kind'] = self.value(_set[-1])
            value_from_seven['kicker'] = []
            value_from_seven['_set'] = _set
            return value_from_seven
        # Three_os_a_Kind
        if value_from_seven['rank'] == 3:
            return value_from_seven

        # Two Pair
        value = 0
        for kind in k_counter.items():
            if kind[1] == 2:
                if Kind.value[kind[0]] > value:
                    value = Kind.value[kind[0]]
                    _set = []
                    for card in seven_cards:
                        if card[1] == kind[0]:
                            _set.append(card)
                    value_from_seven['rank'] = 1
                    value_from_seven['kind'] = self.value(_set[0])
                    value_from_seven['kicker'] = [self.value(sorted(seven_cards.difference(_set), key=self.value)[-1])], [self.value(sorted(seven_cards.difference(_set), key=self.value)[-2])],[self.value(sorted(seven_cards.difference(_set), key=self.value)[-3])]
                    value_from_seven['_set'] = _set

        if value_from_seven['rank'] == 1:
            _value_from_seven = value_from_seven['kind']
            k_counter2 = k_counter.copy()
            k_counter2.pop(_set[0][1])
            value = 0
            for kind in k_counter2.items():
                if kind[1] == 3 or kind[1] == 2:
                    if Kind.value[kind[0]] > value:
                        value = Kind.value[kind[0]]
                        _set2 = []
                        for card in seven_cards:
                            if card[1] == kind[0]:
                                _set2.append(card)
                        _set2 = _set2[:2]
                        value_from_seven['rank'] = 2
                        value_from_seven['kind'] = self.value(_set2[0]) + _value_from_seven
                        value_from_seven['kicker'] = [self.value(sorted(seven_cards.difference(_set), key=self.value)[-1])]
                        value_from_seven['_set'] = _set + _set2


        if value_from_seven['rank'] == 2:
            return value_from_seven

        # One_Pair
        if value_from_seven['rank'] == 1:
            return value_from_seven

        # High_Card
        value_from_seven['rank'] = 0
        value_from_seven['kind'] = self.value(sorted(seven_cards, key=self.value)[-1])
        value_from_seven['kicker'] = [self.value(sorted(seven_cards, key=self.value)[-i]) for i in range(2, 7)]
        value_from_seven['_set'] = [sorted(seven_cards, key=self.value)[-1]]
        return value_from_seven

    def compare(self, value: list):
        min_length = min(len(value[0]), len(value[1]))
        for i in range(min_length):
            if value[0][i] > value[1][i]:
                return True
            elif value[0][i] < value[1][i]:
                return False
        return None



    def simulation(self):
        self.complete()

        player_value = self.evalution(self.table.common.cards[:] + self.table.player.cards[:])

        others_value = []
        for i, opponent in enumerate(self.table.others):
            others_value.append(self.evalution(self.table.common.cards[:] + opponent.cards[:]))


        vectors = []
        for hand in [player_value] + others_value:
            vector = [hand['rank'], hand['kind']]
            for x in hand['kicker']:
                vector.append(x)
            vectors.append(vector)

        hand_values = []
        for opponent in vectors[1:]:
            hand_values.append(self.compare([vectors[0], opponent]))
        if False in hand_values:
            return False
        elif None in hand_values:
            return None
        else:
            return True





if __name__ == '__main__':
    print('\ >>> START PROGRAM\n')

    N = 5000
    win = 0
    lose = 0
    split = 0

    for i in range(N):
        deck = Deck()
        player = Hand([deck.deal('DQ'), deck.deal('S6')])
        othes = [Hand([deck.deal('??'), deck.deal('??')]),
                 Hand([deck.deal('??'), deck.deal('??')]),
                 Hand([deck.deal('??'), deck.deal('??')]),
                 Hand([deck.deal('??'), deck.deal('??')]),
                 Hand([deck.deal('??'), deck.deal('??')]
                      )]
        common = Common([deck.deal('D0'),
                         deck.deal('D4'),
                         deck.deal('S0'),
                         deck.deal('HA'),
                         deck.deal('H7')
                         ])

        table = Table()
        table.deal(deck, common, player, othes)
        #table.show_table()

        simulation = Simulation(table)
        simulation.complete()

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
