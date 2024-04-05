import pandas as pd
from .Event import Event
from .Team import Team


class Game:
    """A class for keeping info about the games"""
    def __init__(self, path_to_json, event_num):
        # self.events = None
        self.home_team = None
        self.guest_team = None
        self.event = None
        self.path_to_json = path_to_json
        self.event_num = event_num

    @staticmethod
    def load_event_by_num(game_df, event_num):
        for event in game_df['events']:
            if(event['eventId']  == str(event_num)):
                return event

    def read_json(self):
        game_df = pd.read_json(self.path_to_json)

        event = Game.load_event_by_num(game_df, self.event_num)
        self.event = Event(event)
        self.home_team = Team(event['home']['teamid'])
        self.guest_team = Team(event['visitor']['teamid'])


    def start(self):
        self.event.show()
