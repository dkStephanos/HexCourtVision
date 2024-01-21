from Game import Game
import easygui

while True:
    game_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/backend/game_raw_data/", title="Select a game file")

    while True:
        print('\nEnter the event (or exit to return to game select): ')
        event = input()
        if(event == "exit"):
            break
        try:
            game = Game(path_to_json=game_path, event_num=event)
            game.read_json()

            game.start()
        except:
            print("Invlid event number, try again.")
