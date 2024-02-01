from django.db import models	
from django.contrib.postgres.fields import ArrayField

class Team(models.Model):
    class Meta:
        app_label = 'ml_nba'
        
    team_id = models.CharField(primary_key=True, max_length=15)
    color = models.CharField(max_length=7)
    name = models.CharField(max_length=25)
    abreviation = models.CharField(max_length=3)

class Player(models.Model):
    class Meta:
        app_label = 'ml_nba'
        
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    player_id = models.CharField(primary_key=True, max_length=15)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    jersey_number = models.IntegerField()
    position = models.CharField(max_length=5)

class Game(models.Model):
    class Meta:
        app_label = 'ml_nba'
        
    game_id = models.CharField(primary_key=True, max_length=15)
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.SET_NULL, null=True)
    visitor_team = models.ForeignKey(Team, related_name="visitor_team", on_delete=models.SET_NULL, null=True)
    game_date = models.CharField(max_length=20)
    final_score = models.CharField(max_length=9)

class Event(models.Model):
    class Meta:
        app_label = 'ml_nba'
        
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
    home_desc = models.CharField(max_length=100)
    visitor_desc = models.CharField(max_length=100)
    score = models.CharField(max_length=9)
    directionality = models.CharField(max_length=5)

class Moment(models.Model):
    class Meta:
        app_label = 'ml_nba'
        
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
    class Meta:
        app_label = 'ml_nba'
        
    candidate_id = models.CharField(primary_key=True, max_length=15)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    classification_type = models.CharField(max_length=20)
    manual_label = models.BooleanField()
    period = models.IntegerField()
    game_clock = models.CharField(max_length=5)
    shot_clock = models.FloatField()
    player_a = models.ForeignKey(Player, related_name="player_a", on_delete=models.SET_NULL, null=True)
    player_a_name = models.CharField(max_length=25)
    player_b = models.ForeignKey(Player, related_name="player_b", on_delete=models.SET_NULL, null=True)
    player_b_name = models.CharField(max_length=25)
    notes = models.CharField(max_length=100)

class CandidateFeatureVector(models.Model):
    class Meta:
        app_label = 'ml_nba'
        
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    classification = models.BooleanField()
    
    # Player Data
    cutter_archetype = models.CharField(max_length=20)
    screener_archetype = models.CharField(max_length=20)

    # Location Data
    cutter_loc_on_pass = models.CharField(max_length=100)
    screener_loc_on_pass = models.CharField(max_length=100)
    ball_loc_on_pass = models.CharField(max_length=100) 
    ball_radius_on_pass = models.CharField(max_length=100) 
    cutter_loc_on_start_approach = models.CharField(max_length=100) 
    screener_loc_on_start_approach = models.CharField(max_length=100) 
    ball_loc_on_start_approach = models.CharField(max_length=100) 
    ball_radius_loc_on_start_approach = models.CharField(max_length=100) 
    cutter_loc_on_end_execution = models.CharField(max_length=100) 
    screener_loc_on_end_execution = models.CharField(max_length=100) 
    ball_loc_on_end_execution = models.CharField(max_length=100) 
    ball_radius_loc_on_end_execution = models.CharField(max_length=100) 
    cutter_loc_on_screen = models.CharField(max_length=100) 
    screener_loc_on_screen = models.CharField(max_length=100) 
    ball_loc_on_screen = models.CharField(max_length=100) 
    ball_radius_on_screen = models.CharField(max_length=100) 

    # Travel Distance Data
    cutter_dist_traveled_approach = models.FloatField() 
    cutter_dist_traveled_execution = models.FloatField() 
    screener_dist_traveled_approach = models.FloatField() 
    screener_dist_traveled_execution = models.FloatField() 
    ball_dist_traveled_approach = models.FloatField() 
    ball_dist_traveled_execution = models.FloatField() 

    # Relative Distance Data
    players_dist_on_pass = models.FloatField() 
    cutter_dist_from_ball_on_pass = models.FloatField() 
    screener_dist_from_ball_on_pass = models.FloatField() 
    players_dist_on_screen = models.FloatField() 
    cutter_dist_from_ball_on_screen = models.FloatField() 
    screener_dist_from_ball_on_screen = models.FloatField() 
    players_dist_on_start_approach = models.FloatField() 
    cutter_dist_from_ball_on_approach = models.FloatField() 
    screener_dist_from_ball_on_approach = models.FloatField() 
    players_dist_on_end_execution = models.FloatField() 
    cutter_dist_from_ball_on_execution = models.FloatField() 
    screener_dist_from_ball_on_execution = models.FloatField() 

    # Speed/Acceleration Data
    cutter_avg_speed_approach = models.FloatField() 
    cutter_avg_speed_execution = models.FloatField() 
    screener_avg_speed_approach = models.FloatField() 
    screener_avg_speed_execution = models.FloatField() 
    ball_avg_speed_approach = models.FloatField() 
    ball_avg_speed_execution = models.FloatField() 

    # Linear Regression Data
    slope_of_cutter_trajectory_approach = models.FloatField() 
    intercept_of_cutter_trajectory_approach = models.FloatField() 
    slope_of_cutter_trajectory_execution = models.FloatField() 
    intercept_of_cutter_trajectory_execution = models.FloatField() 
    slope_of_screener_trajectory_approach = models.FloatField() 
    intercept_of_screener_trajectory_approach = models.FloatField() 
    slope_of_screener_trajectory_execution = models.FloatField() 
    intercept_of_screener_trajectory_execution = models.FloatField() 
    slope_of_ball_trajectory_approach = models.FloatField()
    intercept_of_ball_trajectory_approach = models.FloatField()
    slope_of_ball_trajectory_execution = models.FloatField() 
    intercept_of_ball_trajectory_execution = models.FloatField() 

    # Play Data
    offset_into_play = models.IntegerField() 
    pass_duration = models.IntegerField() 
    num_players_past_half_court = models.IntegerField() 
    is_inbounds_pass = models.BooleanField()

class CandidateHexmap(models.Model):
    class Meta:
        app_label = 'ml_nba'
        
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    hexmap = ArrayField(models.CharField(max_length=10, blank=True))
    cluster = models.IntegerField()
    
