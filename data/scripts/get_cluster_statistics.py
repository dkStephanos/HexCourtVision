from data.models import Candidate, CandidateHexmap

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

    for map in hexmaps:
        clusters[str(map['cluster'])].append((map, Candidate.objects.filter(candidate_id=map['candidate_id']).values()))

    print('Cluster populations:')
    for key, value in clusters.items():
        print(f'Cluster {key} size: {len(value)}')

        