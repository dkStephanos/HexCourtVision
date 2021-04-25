import os
import cv2
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import kernel_metrics

def run():
    n_clusters = 10
    image_dim = (480, 640, 3)
    hex_dir = 'C:\\Users\\Stephanos\\Documents\\Dev\\NBAThesis\\NBA_Thesis\\static\\data\\hexmaps30'
    directory = os.fsencode(hex_dir)
    image_names = []
    images = []
    hexmaps = []
    '''
    print("Creating feature vectors from hexmaps -----------\n\n")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        image = cv2.imread(hex_dir + '\\' + filename)
        images.append(image)
        hexmaps.append(image.flatten())

    print("Running dimensionality reduction on dataset ----------")
    print(hexmaps[0].shape)
    pca = PCA()
    hexmaps = pca.fit_transform(hexmaps)
    np.save("static/data/test/hexmaps", hexmaps)
    print(hexmaps[0].shape)
    '''
    print("Loading hexmap representations from file ----------------\n\n")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        image = cv2.imread(hex_dir + '\\' + filename)
        image_names.append(filename)
        images.append(image)
    hexmaps = np.load("static/data/test/hexmaps30.npy")
    print(hexmaps)
    '''
    print("Get elbow plot for hexmap clusters ----------------\n\n")
    distortions = []
    for i in range(1, 31):
        print(f"starting fit for {i} clusters")
        km = KMeans(
            n_clusters=i, init='random',
            n_init=10, max_iter=300,
            tol=1e-04, random_state=0
        )
        km.fit(hexmaps)
        distortions.append(km.inertia_)

    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 31), distortions, marker='o')
    plt.xticks(range(1, 31))
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()
    
    print("Get the silhouette coefficients for clusters ----------------\n\n")
    # A list holds the silhouette coefficients for each k
    silhouette_coefficients = []

    for k in range(2, 31):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(hexmaps)
        score = silhouette_score(hexmaps, kmeans.labels_)
        silhouette_coefficients.append(score)

    plt.style.use("fivethirtyeight")
    plt.plot(range(2, 31), silhouette_coefficients)
    plt.xticks(range(2, 31))
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()
    
    print("Running the KMeans clustering model -----------\n\n")
    kmeans = KMeans(n_clusters=n_clusters,init='random')
    y_km = kmeans.fit_predict(hexmaps)
    distortion = ((hexmaps - kmeans.cluster_centers_[y_km])**2.0).sum(axis=1)

    labels = pd.DataFrame({'cluster':kmeans.labels_, 'distortion':distortion})
    print(labels['cluster'].value_counts())

    print("Get the samples closest to the centroids")
    for cluster in range(0,n_clusters):
        print(f"\nThe closest samples to cluster {cluster}")
        d = kmeans.transform(hexmaps)[:, cluster]
        print(labels.loc[labels['cluster'] == cluster, 'distortion'].sum())
        ind = np.argsort(d)[::-1][:3]
        
        for i in list(ind):
            print(i)
            cv2.imshow('dst_rt', images[i])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    '''
    for i in [416,452,355,24,75,329]:
        print(image_names[i])
        cv2.imshow('dst_rt', images[i])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    