import pandas as pd
from collections import Counter
from ml_nba.models import Candidate, Team, Player, CandidateHexmap

class ClusterStats:
    def __init__(self):
        self.clusters = {str(i): [] for i in range(9)}
        self.hexmaps = CandidateHexmap.objects.all().values()
        self.populate_clusters()

    def populate_clusters(self):
        for map in self.hexmaps:
            candidate = Candidate.objects.filter(candidate_id=map['candidate_id']).values()[0]
            screener = Player.objects.filter(player_id=candidate['player_a_id']).values()[0]
            cutter = Player.objects.filter(player_id=candidate['player_b_name']).values()[0] # Ensure this is the correct field for 'cutter'
            team = Team.objects.filter(team_id=screener['team_id']).values()[0]
            self.clusters[str(map['cluster'])].append((map, candidate, team, screener, cutter))

    def print_cluster_populations(self):
        print('Cluster populations:')
        for key, value in self.clusters.items():
            print(f'Cluster {key} size: {len(value)}')

    def print_team_breakdown(self, team_abbr=None):
        if team_abbr:
            self.print_breakdown_for_team(team_abbr)
        else:
            self.print_breakdown_by_team()

    def print_breakdown_by_team(self):
        print('Breakdown by team:')
        for key, cluster in self.clusters.items():
            teams = [action[2]['abbreviation'] for action in cluster]
            print(f'Team totals for cluster {key}: {Counter(teams).items()}')

    def print_breakdown_for_team(self, team_abbr):
        print(f'Breakdown for team: {team_abbr}')
        counts = Counter([key for key, cluster in self.clusters.items() for action in cluster if action[2]['abbreviation'] == team_abbr])
        print(f'Cluster totals for team {team_abbr}: {dict(counts)}')

    def print_player_breakdown(self, player_name):
        screener_counts, cutter_counts = self.get_player_breakdown(player_name)
        print(f'Breakdown for player: {player_name}')
        print('As screener:', screener_counts)
        print('As cutter:', cutter_counts)

    def get_player_breakdown(self, player_name):
        screener_counts, cutter_counts = Counter(), Counter()
        for key, cluster in self.clusters.items():
            for action in cluster:
                if action[3]['name'] == player_name:  # Assuming 'name' is the correct field
                    screener_counts[key] += 1
                if action[4]['name'] == player_name:
                    cutter_counts[key] += 1
        return dict(screener_counts), dict(cutter_counts)

# Example usage:
analysis = ClusterAnalysis()
analysis.print_cluster_populations()
analysis.print_team_breakdown('GSW')
analysis.print_player_breakdown('Stephen Curry')
