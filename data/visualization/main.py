from Game import Game

games = {"1": 'C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.11.2015.GSW.at.BOS/0021500336.json',
         "2": "C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.25.2015.LAC.at.LAL/0021500440.json",
         "3": "C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.30.2015.DEN.at.POR/0021500482.json",
         "4": "C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.30.2015.GSW.at.DAL/0021500480.json",
         "5": "C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.31.2015.PHX.at.OKC/0021500488.json",
         "6": "C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.06.2015.MIL.at.NYK/0021500079.json"
        }

while True:
    print('Enter the path to the game you would like to see from the following list: \n1) GSWatBOS\n2) LACatLAL\n3) DENatPOR\n4) GSWatDAL\n5) PHXatOKC\n6) MILatNYK')
    print('\nEnter the game (or exit): ')
    selection = input()
    if(selection == "exit"):
        exit()
    path = games[selection]

    while True:
        print('\nEnter the event (or exit to return to game select): ')
        event = input()
        if(event == "exit"):
            break
        game = Game(path_to_json=path, event_num=event)
        game.read_json()

        game.start()
