from django.db import models	

class Team(models.Model):
    team_id = models.CharField(primary_key=True, max_length=15)
    color = models.CharField(max_length=7)
    name = models.CharField(max_length=25)
    abreviation = models.CharField(max_length=3)

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    player_id = models.CharField(primary_key=True, max_length=15)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    jersey_number = models.IntegerField()
    position = models.CharField(max_length=5)

class Game(models.Model):
    game_id = models.CharField(primary_key=True, max_length=15)
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.SET_NULL, null=True)
    visitor_team = models.ForeignKey(Team, related_name="visitor_team", on_delete=models.SET_NULL, null=True)
    game_date = models.CharField(max_length=20)
    final_score = models.CharField(max_length=9)

class Event(models.Model):
    event_id = models.CharField(primary_key=True, max_length=15)
    game = models.ForeignKey(Game, related_name="events", on_delete=models.SET_NULL, null=True)
    possesion_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    player_1 = models.ForeignKey(Player, related_name="player_1", on_delete=models.SET_NULL, null=True)
    player_2 = models.ForeignKey(Player, related_name="player_2", on_delete=models.SET_NULL, null=True)
    player_3 = models.ForeignKey(Player, related_name="player_3", on_delete=models.SET_NULL, null=True)
    event_num = models.IntegerField()
    event_msg_type = models.IntegerField()
    event_action_type = models.IntegerField()
    period = models.IntegerField()
    period_time = models.CharField(max_length=5)
    home_desc = models.CharField(max_length=50)
    visitor_desc = models.CharField(max_length=50)
    score = models.CharField(max_length=7)
    directionality = models.CharField(max_length=5)

class Moment(models.Model):
    moment_id = models.CharField(primary_key=True, max_length=15)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    x_loc = models.FloatField()
    y_loc = models.FloatField()
    radius = models.FloatField(null=True)
    index = models.IntegerField()
    game_clock = models.FloatField()
    shot_clock = models.FloatField()

class Candidate(models.Model):
    candidate_id = models.CharField(primary_key=True, max_length=15)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    classification_type = models.CharField(max_length=20)
    manual_label = models.BooleanField()
    period = models.IntegerField()
    game_clock = models.CharField(max_length=5)
    shot_clock = models.FloatField()
    player_a = models.ForeignKey(Player, related_name="player_a", on_delete=models.SET_NULL, null=True)
    player_b = models.ForeignKey(Player, related_name="player_b", on_delete=models.SET_NULL, null=True)

