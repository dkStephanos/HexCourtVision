import os
import cv2
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from data.models import Game
from data.models import Player
from data.models import Event
from data.models import Moment
from data.models import Candidate
import matplotlib.pyplot as plt
import math, os

from data.preprocessing.utilities.DataUtil import DataUtil
from data.preprocessing.utilities.FeatureUtil import FeatureUtil
from data.preprocessing.utilities.GraphUtil import GraphUtil

def get_hexbins(target_candidate):
    # Collects moments for single candidate
    moments = pd.DataFrame(list(Moment.objects.filter(event_id=target_candidate['event_id']).values()))

    # Collects players for single candidate
    screener = Player.objects.values().get(player_id=target_candidate['player_a_id'])
    cutter = Player.objects.values().get(player_id=target_candidate['player_b_id'])

    # Trim the moments data around the pass
    game_clock = DataUtil.convert_timestamp_to_game_clock(target_candidate['game_clock'])
    trimmed_moments = moments[(moments.game_clock > game_clock - 2) & (moments.game_clock < game_clock + 2)]

    # If the data occurs past half-court (x > 47), rotate the points about the center of the court so features appear consistent 
    if(trimmed_moments.iloc[math.ceil(len(trimmed_moments)/2)]['x_loc'] > 47.0):
        trimmed_moments = FeatureUtil.rotate_coordinates_around_center_court(trimmed_moments)

    # Isolate cutter, screener and ball from trimmed_moments
    cutter_df = trimmed_moments[trimmed_moments['player_id'] == cutter['player_id']][['x_loc', 'y_loc']]
    screener_df = trimmed_moments[trimmed_moments['player_id'] == screener['player_id']][['x_loc', 'y_loc']]
    ball_df = trimmed_moments[trimmed_moments['player_id'].isna()][['x_loc', 'y_loc']]

    # Offset y_loc data to work with hexbin
    screener_hex_df = screener_df.copy(deep=True)
    cutter_hex_df = cutter_df.copy(deep=True)
    ball_hex_df = ball_df.copy(deep=True)
    screener_hex_df['y_loc'] = screener_hex_df['y_loc'] - 50.0
    cutter_hex_df['y_loc'] = cutter_hex_df['y_loc'] - 50.0
    ball_hex_df['y_loc'] = ball_hex_df['y_loc'] - 50.0
    ax = GraphUtil.draw_court()	
    screener_hexbin = ax.hexbin(x=screener_hex_df['x_loc'], y=screener_hex_df['y_loc'], cmap=plt.cm.Greens, mincnt=1, gridsize=50, extent=(0,94,-50,0))
    cutter_hexbin = ax.hexbin(x=cutter_hex_df['x_loc'], y=cutter_hex_df['y_loc'], cmap=plt.cm.Blues, mincnt=1, gridsize=50, extent=(0,94,-50,0))
    ball_hexbin = ax.hexbin(x=ball_hex_df['x_loc'], y=ball_hex_df['y_loc'], cmap=plt.cm.Reds, mincnt=1, gridsize=50, extent=(0,94,-50,0))

    return [*screener_hexbin.get_array(), *cutter_hexbin.get_array(), *ball_hexbin.get_array()]

def run():
    n_clusters = 9
    hex_dir = 'C:\\Users\\Stephanos\\Documents\\Dev\\NBAThesis\\NBA_Thesis\\static\\data\\hexmaps'
    directory = os.fsencode(hex_dir)
    images = []
    candidates_hexbins = []
    lengths = []
    filenames = []

    print("Loading hexmap representations from file ----------------\n\n")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filenames.append(filename[:-11])
        image = cv2.imread(hex_dir + '\\' + filename)
        images.append(image)

    print(filenames)

    # Creating hexbin dataframes for DHO's
    for game in Game.objects.all():
        events = Event.objects.filter(game=game)
        for event in events:
            next_candidates = Candidate.objects.filter(event=event).values()
            for target_candidate in next_candidates:
                if(target_candidate['manual_label'] == True and target_candidate['candidate_id'] in filenames):
                    try:
                        hexbins = get_hexbins(target_candidate)
                        candidates_hexbins.append(hexbins)
                        lengths.append(len(hexbins))
                    except Exception as e:
                        print(f"Issue at candidate: {target_candidate['candidate_id']}")
    
    max_len = max(lengths)
    for candidate in candidates_hexbins:
        num_to_pad = max_len - len(candidate)
        if(num_to_pad > 0):
            for i in range(num_to_pad):
                candidate.append(0)
    '''
    print("Get elbow plot for hexmap clusters ----------------\n\n")
    distortions = []
    for i in range(1, 15):
        print(f"starting fit for {i} clusters")
        km = KMeans(
            n_clusters=i, init='random',
            n_init=10, max_iter=300,
            tol=1e-04, random_state=0
        )
        km.fit(candidates_hexbins)
        distortions.append(km.inertia_)

    #plt.style.use("fivethirtyeight")
    plt.plot(range(1, 15), distortions, marker='o')
    plt.xticks(range(1, 15))
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()
    '''
    print("Get the silhouette coefficients for clusters ----------------\n\n")
    # A list holds the silhouette coefficients for each k
    silhouette_coefficients = []

    for k in range(2, 15):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(candidates_hexbins)
        score = silhouette_score(candidates_hexbins, kmeans.labels_)
        silhouette_coefficients.append(score)

    plt.style.use("fivethirtyeight")
    plt.plot(range(2, 15), silhouette_coefficients)
    plt.xticks(range(2, 15))
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()
    
    print("Running the KMeans clustering model -----------\n\n")
    kmeans = KMeans(n_clusters=n_clusters,init='random')
    kmeans.fit(candidates_hexbins)
    Z = kmeans.predict(candidates_hexbins)

    print("Get the samples closest to the centroids")
    for cluster in range(0,n_clusters):
        print(f"\nThe closest samples to cluster {cluster}")
        d = kmeans.transform(candidates_hexbins)[:, cluster]
        ind = np.argsort(d)[::-1][:3]
        
        for i in list(ind):
            cv2.imshow('dst_rt', images[i])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
