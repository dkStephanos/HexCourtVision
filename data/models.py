from django.db import models	

class Constant(models.Model):
    NORMALIZATION_COEF = 7
    PLAYER_CIRCLE_SIZE = 12 / NORMALIZATION_COEF
    INTERVAL = 10
    DIFF = 6
    X_MIN = 0
    X_MAX = 100
    Y_MIN = 0
    Y_MAX = 50
    COL_WIDTH = 0.3
    SCALE = 1.65
    FONTSIZE = 6
    X_CENTER = X_MAX / 2 - DIFF / 1.5 + 0.10
    Y_CENTER = Y_MAX - DIFF / 1.5 - 0.35

class Ball(models.Model):
    x = models.FloatField() 
    y = models.FloatField()
    radius = models.FloatField()
    color = models.models.CharField(max_length=7)

class Team(models.Model):
    team_id = models.IntegerField()
    color = models.CharField(max_length=7)
    name = models.CharField(max_length=3)

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    player_id = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

class Moment(models.Model):
    quarter = models.IntegerField()  # Hardcoded position for quarter in json
    game_clock = models.FloatField()  # Hardcoded position for game_clock in json
    shot_clock = models.FloatField()  # Hardcoded position for shot_clock in json
    ball = models.ForeignKey(Ball, on_delete=models.SET_NULL, null=True)
    players = models.ManyToManyField(Player)

class Event(models.Model):
    event_id = models.IntegerField()
    moments = models.ForeignKey(Moment, on_delete=models.SET_NULL, null=True)
    home_players = models.ForeignKey(Player, related_name="home_players", on_delete=models.SET_NULL, null=True)
    guest_players = models.ForeignKey(Player, related_name="guest_players", on_delete=models.SET_NULL, null=True)

class Game(models.Model):
    game_id = models.IntegerField()
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.SET_NULL, null=True)
    guest_team = models.ForeignKey(Team, related_name="guest_team", on_delete=models.SET_NULL, null=True)
    events = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)