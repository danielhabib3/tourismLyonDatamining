# import the csv file
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import folium
import os
from sklearn.cluster import KMeans
import datamining as dm  # contains clean_data, generate_map
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors



file_path = './data/flickr_data2_cleaned.csv'

# List of files to delete if they exist
files_to_delete = ['./map.html', './elbow.png', './distance_to_4th_nearest_point.png', './mapLargestCluster.html']

# Loop through the list and delete each file if it exists
for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)

# df has to contain 157842 rows
if not(os.path.exists(file_path)):
    print('Data file not found. Cleaning data...')
    df = dm.clean_data('./data/flickr_data2.csv')
else:
    print('Data file found. Reading data...')
    df = pd.read_csv(file_path, low_memory=False)

df_cluster = df[['lat', 'long']]  # Extract the coordinates for clustering

# df = dm.kmeans_algorithm(df, 100)  # Apply the KMeans algorithm



# #_______________________________________________________________________________________________________________________
# # # Calculate the distance to the fourth nearest point for each point
# # # Extract the coordinates
# # coords = df[['lat', 'long']].values

# # # Fit the NearestNeighbors model
# # nbrs = NearestNeighbors(n_neighbors=5).fit(coords)
# # distances, indices = nbrs.kneighbors(coords)

# # # The fourth nearest point is at index 4 (0-based index)
# # fourth_distances = distances[:, 4]

# # # Plot the distances
# # plt.figure(figsize=(10, 6))
# # plt.plot(range(len(fourth_distances)), sorted(fourth_distances, reverse=True))
# # plt.xlabel('Points')
# # plt.ylabel('Distance to 4th Nearest Point')
# # plt.title('Distance to 4th Nearest Point for Each Point')
# # plt.savefig('distance_to_4th_nearest_point.png')

# # _______________________________________________________________________________________________________________________

# # get the value of distance from the plot when it is stable
# stable_distance = 0.0004
# print(f'Stable distance: {stable_distance}')


# dbscan = DBSCAN(eps=stable_distance, min_samples=5)
# dbscan.fit(df_cluster)
# # associated cluster labels
# df['dbscan_cluster'] = dbscan.labels_

# # number of clusters
# n_clusters = len(set(df['dbscan_cluster'])) - (1 if -1 in df['dbscan_cluster'] else 0)
# print(f"Number of clusters: {n_clusters}")
# # number of noise points
# n_noise = list(df['dbscan_cluster']).count(-1)
# print(f"Number of noise points: {n_noise}")



# coordinates = list(set(zip(df['lat'], df['long'], df['dbscan_cluster'])))
# dm.generate_map(coordinates, 1000)  # Générer la carte

# # get the cluster with the most points
# largest_cluster = df['dbscan_cluster'].value_counts().idxmax()
# print(f"Largest cluster: {largest_cluster}")

# # reapply the dbscan algorithm on the largest cluster
# df_largest_cluster = df[df['dbscan_cluster'] == largest_cluster][['lat', 'long']]
# df_largest = df_largest_cluster.copy()

# #_______________________________________________________________________________________________________________________
# # Extract the coordinates
# # coords_vieuxLyon = df_largest[['lat', 'long']].values

# # # Fit the NearestNeighbors model
# # nbrs_vieuxLyon = NearestNeighbors(n_neighbors=5).fit(coords_vieuxLyon)
# # distances_vieuxLyon, indices_vieuxLyon = nbrs_vieuxLyon.kneighbors(coords_vieuxLyon)

# # # The fourth nearest point is at index 4 (0-based index)
# # fourth_distances_vieuxLyon = distances_vieuxLyon[:, 4]

# # # Plot the distances
# # plt.figure(figsize=(10, 6))
# # plt.plot(range(len(fourth_distances_vieuxLyon)), sorted(fourth_distances_vieuxLyon, reverse=True))
# # plt.xlabel('Points')
# # plt.ylabel('Distance to 4th Nearest Point')
# # plt.title('Distance to 4th Nearest Point for Each Point')
# # plt.savefig('vieuxLyon_distance_to_4th_nearest_point.png')

# # _______________________________________________________________________________________________________________________

# dbscan_vieuxLyon = DBSCAN(eps=0.009, min_samples=4)
# dbscan_vieuxLyon.fit(df_largest_cluster)
# df_largest['dbscan_cluster'] = dbscan_vieuxLyon.labels_

# # number of clusters
# n_clusters_vieuxLyon = len(set(df_largest['dbscan_cluster'])) - (1 if -1 in df_largest['dbscan_cluster'] else 0)
# print(f"Number of clusters: {n_clusters_vieuxLyon}")
# # number of noise points
# n_noise_vieuxLyon = list(df_largest['dbscan_cluster']).count(-1)
# print(f"Number of noise points: {n_noise_vieuxLyon}")

# coordinates_vieuxLyon = list(set(zip(df_largest['lat'], df_largest['long'], df_largest['dbscan_cluster'])))
# dm.generate_map(coordinates_vieuxLyon, 1000, "mapLargestCluster.html")  # Générer la carte



















