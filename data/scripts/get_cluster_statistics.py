from data.models import Candidate, Team, Player, CandidateHexmap
from collections import Counter

def run():
    clusters = {
        '0': [],
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
        '7': [],
        '8': [],
    }
    hexmaps = CandidateHexmap.objects.all().values()

    # hexmap tuple = (map, candidate, team, screener, cutter)
    for map in hexmaps:
        candidate = Candidate.objects.filter(candidate_id=map['candidate_id']).values()[0]
        screener = Player.objects.filter(player_id=candidate['player_a_id']).values()[0]
        cutter = Player.objects.filter(player_id=candidate['player_b_id']).values()[0]
        team = Team.objects.filter(team_id=screener['team_id']).values()[0]
        clusters[str(map['cluster'])].append((map, candidate, team, screener, cutter))

    print('Cluster populations:')
    for key, value in clusters.items():
        print(f'Cluster {key} size: {len(value)}')

    print('Breakdown by team:')
    teams = []
    for key, cluster in clusters.items():
        for action in cluster:
            teams.append(action[2]['abreviation'])
        print(f'Team totals for cluster: {key}')
        print(Counter(teams).items())
        teams = []

        