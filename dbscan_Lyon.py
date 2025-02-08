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
files_to_delete = ['./maps/map.html', './elbow_charts/elbow.png', './elbow_charts/distance_to_4th_nearest_point.png', './maps/mapLargestCluster.html', './maps/mapCluster.html']

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



#_______________________________________________________________________________________________________________________
# # Calculate the distance to the fourth nearest point for each point
# # Extract the coordinates
# coords = df[['lat', 'long']].values

# # Fit the NearestNeighbors model
# nbrs = NearestNeighbors(n_neighbors=5).fit(coords)
# distances, indices = nbrs.kneighbors(coords)

# # The fourth nearest point is at index 4 (0-based index)
# fourth_distances = distances[:, 4]

# # Plot the distances
# plt.figure(figsize=(10, 6))
# plt.plot(range(len(fourth_distances)), sorted(fourth_distances, reverse=True))
# plt.xlabel('Points')
# plt.ylabel('Distance to 4th Nearest Point')
# plt.title('Distance to 4th Nearest Point for Each Point')
# plt.savefig('./elbow_charts/distance_to_4th_nearest_point.png')

# _______________________________________________________________________________________________________________________

# get the value of distance from the plot when it is stable
stable_distance = 0.0004
print(f'Stable distance: {stable_distance}')


dbscan = DBSCAN(eps=stable_distance, min_samples=5)
dbscan.fit(df_cluster)
# associated cluster labels
df['dbscan_cluster'] = dbscan.labels_

# number of clusters
n_clusters = len(set(df['dbscan_cluster'])) - (1 if -1 in df['dbscan_cluster'] else 0)
print(f"Number of clusters: {n_clusters}")
# number of noise points
n_noise = list(df['dbscan_cluster']).count(-1)
print(f"Number of noise points: {n_noise}")



coordinates = list(set(zip(df['lat'], df['long'], df['dbscan_cluster'])))
dm.generate_map(coordinates, 1000, "./maps/mapCluster.html")  # Générer la carte

# get the cluster with the most points
largest_cluster = df['dbscan_cluster'].value_counts().idxmax()
print(f"Largest cluster: {largest_cluster}")

# reapply the dbscan algorithm on the largest cluster
df_largest_cluster = df[df['dbscan_cluster'] == largest_cluster][['lat', 'long']]
df_largest = df_largest_cluster.copy()

# save the largest cluster in a csv file
df_largest.to_csv('./data/flickr_data2_largest_cluster.csv', index=False)


# print the number of clusters having less than 10 points in them
print(f"Number of clusters with less than 50 points: {df['dbscan_cluster'].value_counts()[df['dbscan_cluster'].value_counts() < 50].count()}")

# create a new dataframe without the clusters having less than 50 points
filtered_clusters = df['dbscan_cluster'].value_counts()[df['dbscan_cluster'].value_counts() >= 50].index

# print the number of clusters after filtering
filtered_df = df[df['dbscan_cluster'].isin(filtered_clusters)]
n_clusters_filtered = len(set(filtered_df['dbscan_cluster'])) - (1 if -1 in filtered_df['dbscan_cluster'] else 0)
print(f"Number of clusters after filtering: {n_clusters_filtered}")

coordinates_filtered = list(set(zip(filtered_df['lat'], filtered_df['long'], filtered_df['dbscan_cluster'])))
dm.generate_map(coordinates_filtered, 5000, "./maps/mapFilteredCluster.html")  # Générer la

# save the filtered clusters in a csv file without the largest cluster and noise points, including the labels
# Reorganize the labels to be consecutive integers starting from 1
unique_labels = filtered_df['dbscan_cluster'].unique()
label_mapping = {label: idx + 1 for idx, label in enumerate(unique_labels)}

filtered_df.loc[:, 'dbscan_cluster'] = filtered_df['dbscan_cluster'].map(label_mapping)

df_filtered = filtered_df[(filtered_df['dbscan_cluster'] != label_mapping[largest_cluster]) & (filtered_df['dbscan_cluster'] != label_mapping[-1])][['lat', 'long', 'dbscan_cluster']]


df_filtered.to_csv('./data/flickr_data2_filtered_clusters.csv', index=False)




