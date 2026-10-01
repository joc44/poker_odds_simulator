






if __name__ == '__main__':
    print('\ >>> START PROGRAM\n')

    N = 1000
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

        simulation = Simulation(table)
        result = simulation.simulation()
        if result == True:
            win +=1
        elif result == False:
            lose += 1
        else:
            split += 1

    print('Win:\t', round(win/N*100, 2), ' %')
    print('Lose:\t', round(lose / N * 100, 2), ' %')
    print('Split:\t', round(split / N * 100, 2), ' %')
    print()
