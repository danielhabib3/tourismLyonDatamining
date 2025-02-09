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



file_path = './data/flickr_data2_largest_cluster.csv'

# List of files to delete if they exist
files_to_delete = ['./maps/map.html', './elbow_charts/elbow.png', './elbow_charts/distance_to_4th_nearest_point.png', './maps/mapLargestCluster.html', './maps/mapCluster.html']

# Loop through the list and delete each file if it exists
for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)

# df has to contain 157842 rows
if not(os.path.exists(file_path)):
    print('Data file not found. Cleaning data...')
    # end program if the file does not exist
    exit()
else:
    print('Data file found. Reading data...')
    df_largest = pd.read_csv(file_path, low_memory=False)


print(df_largest.head())

#_______________________________________________________________________________________________________________________
# Extract the coordinates
# coords_vieuxLyon = df_largest[['lat', 'long']].values

# # Fit the NearestNeighbors model
# nbrs_vieuxLyon = NearestNeighbors(n_neighbors=5).fit(coords_vieuxLyon)
# distances_vieuxLyon, indices_vieuxLyon = nbrs_vieuxLyon.kneighbors(coords_vieuxLyon)

# # The fourth nearest point is at index 4 (0-based index)
# fourth_distances_vieuxLyon = distances_vieuxLyon[:, 4]

# # Plot the distances
# plt.figure(figsize=(10, 6))
# plt.plot(range(len(fourth_distances_vieuxLyon)), sorted(fourth_distances_vieuxLyon, reverse=True))
# plt.xlabel('Points')
# plt.ylabel('Distance to 4th Nearest Point')
# plt.title('Distance to 4th Nearest Point for Each Point')
# plt.savefig('./elbow_charts/vieuxLyon_distance_to_4th_nearest_point.png')

# _______________________________________________________________________________________________________________________

df_sample = df_largest.sample(n=30000, random_state=42)

dbscan_vieuxLyon = DBSCAN(eps=0.00009, min_samples=4)
dbscan_vieuxLyon.fit(df_sample[['lat', 'long']])
df_sample['dbscan_cluster'] = dbscan_vieuxLyon.labels_

# number of clusters
n_clusters_vieuxLyon = len(set(df_sample['dbscan_cluster'])) - (1 if -1 in df_sample['dbscan_cluster'] else 0)
print(f"Number of clusters: {n_clusters_vieuxLyon}")
# number of noise points
n_noise_vieuxLyon = list(df_sample['dbscan_cluster']).count(-1)
print(f"Number of noise points: {n_noise_vieuxLyon}")

# Filter out clusters with less than 20 points
filtered_clusters = df_sample['dbscan_cluster'].value_counts()[df_sample['dbscan_cluster'].value_counts() >= 50].index
filtered_df_sample = df_sample[df_sample['dbscan_cluster'].isin(filtered_clusters)]

coordinates_vieuxLyon = list(set(zip(filtered_df_sample['lat'], filtered_df_sample['long'], filtered_df_sample['dbscan_cluster'])))

print(f"Number of clusters with less than 50 points: {df_sample['dbscan_cluster'].value_counts()[df_sample['dbscan_cluster'].value_counts() < 50].count()}")



# dm.generate_map(coordinates_vieuxLyon, 5000, "./maps/mapLargestCluster.html")  # Générer la carte


# save the filtered data to a csv file without the noise points
filtered_df_sample = filtered_df_sample[filtered_df_sample['dbscan_cluster'] != -1]

# print the number of clusters
print('Number of clusters: ', len(filtered_df_sample['dbscan_cluster'].unique()))

# Make cluster numbers consecutive starting from 128
unique_clusters = filtered_df_sample['dbscan_cluster'].unique()
cluster_mapping = {old_cluster: new_cluster for new_cluster, old_cluster in enumerate(unique_clusters, 128)}
filtered_df_sample['dbscan_cluster'] = filtered_df_sample['dbscan_cluster'].map(cluster_mapping)

# print the cluster numbers and the number of points in each cluster
for cluster in filtered_df_sample['dbscan_cluster'].unique():
    print(f"Cluster {cluster}: {filtered_df_sample[filtered_df_sample['dbscan_cluster'] == cluster].shape[0]} points")

filtered_df_sample.to_csv('./data/flickr_data2_largest_cluster_filtered.csv', index=False)




















