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

    # print('Cluster populations:')
    # for key, value in clusters.items():
    #     print(f'Cluster {key} size: {len(value)}')

    # print('Breakdown by team:')
    # teams = []
    # for key, cluster in clusters.items():
    #     for action in cluster:
    #         teams.append(action[2]['abreviation'])
    #     print(f'Team totals for cluster: {key}')
    #     print(Counter(teams).items())
    #     teams = []

    # print('Breakdown for team:')
    # team = 'GSW'
    # counts = {}
    # for key, cluster in clusters.items():
    #     for action in cluster:
    #         if (action[2]['abreviation'] == team):
    #             if (key in counts):
    #                 counts[key] += 1
    #             else:
    #                 counts[key] = 1
    # print(f'Cluster totals for team:')
    # print(counts)

    # print('Breakdown by Screener:')
    # screeners = []
    # for key, cluster in clusters.items():
    #     for action in cluster:
    #         screeners.append(action[3]['position'])
    #     print(f'Screener archetype totals for cluster: {key}')
    #     print(Counter(screeners).items())
    #     screeners = []

    # print('Breakdown by Cutter:')
    # screeners = []
    # for key, cluster in clusters.items():
    #     for action in cluster:
    #         screeners.append(action[4]['position'])
    #     print(f'Cutter archetype totals for cluster: {key}')
    #     print(Counter(screeners).items())
    #     screeners = []

    print('Breakdown for player:')
    player = 'Stephen Curry'
    screener_counts = {}
    cutter_counts = {}
    for key, cluster in clusters.items():
        for action in cluster:
            if (action[1]['player_a_name'] == player):
                if (key in screener_counts):
                    screener_counts[key] += 1
                else:
                    screener_counts[key] = 1
            if (action[1]['player_b_name'] == player):
                if (key in cutter_counts):
                    cutter_counts[key] += 1
                else:
                    cutter_counts[key] = 1
    print(f'Cluster totals for player:')
    print(screener_counts)
    print(cutter_counts)

    print('Breakdown for player:')
    player = 'Kobe Bryant'
    screener_counts = {}
    cutter_counts = {}
    for key, cluster in clusters.items():
        for action in cluster:
            if (action[1]['player_a_name'] == player):
                if (key in screener_counts):
                    screener_counts[key] += 1
                else:
                    screener_counts[key] = 1
            if (action[1]['player_b_name'] == player):
                if (key in cutter_counts):
                    cutter_counts[key] += 1
                else:
                    cutter_counts[key] = 1
    print(f'Cluster totals for player:')
    print(screener_counts)
    print(cutter_counts)

    print('Breakdown for player:')
    player = 'Chris Bosh'
    screener_counts = {}
    cutter_counts = {}
    for key, cluster in clusters.items():
        for action in cluster:
            if (action[1]['player_a_name'] == player):
                if (key in screener_counts):
                    screener_counts[key] += 1
                else:
                    screener_counts[key] = 1
            if (action[1]['player_b_name'] == player):
                if (key in cutter_counts):
                    cutter_counts[key] += 1
                else:
                    cutter_counts[key] = 1
    print(f'Cluster totals for player:')
    print(screener_counts)
    print(cutter_counts)