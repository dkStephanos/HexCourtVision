from Game import Game

game = Game(path_to_json='C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA-Player-Movements/data/11.19.2015.GSW.at.LAC/0021500177.json', event_index=13)
game.read_json()

game.start()

while True:
    print('Enter the path to the game you would like to see: ')
    path = input()
    print('\nEnter the event: ')
    event = input()

    game = Game(path_to_json=path, event_index=event)
    game.read_json()

    game.start()
