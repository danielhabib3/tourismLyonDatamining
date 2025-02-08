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



file_path_Lyon = './data/flickr_data2_filtered_clusters.csv'
file_path_VieuxLyon = './data/flickr_data2_largest_cluster_filtered.csv'

# List of files to delete if they exist
files_to_delete = ['./maps/map.html', './elbow_charts/elbow.png', './elbow_charts/distance_to_4th_nearest_point.png', './maps/mapLargestCluster.html', './maps/mapCluster.html']

# Loop through the list and delete each file if it exists
for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)

# df has to contain 157842 rows
if not(os.path.exists(file_path_Lyon) or os.path.exists(file_path_VieuxLyon)):
    print('Data file not found. Cleaning data...')
    # end program if the file does not exist
    exit()
else:
    print('Data file found. Reading data...')
    df_Lyon = pd.read_csv(file_path_Lyon, low_memory=False)
    df_VieuxLyon = pd.read_csv(file_path_VieuxLyon, low_memory=False)

# merge the two dataframes
df = pd.concat([df_Lyon, df_VieuxLyon])

# create coordinates to generate the map
coordinates_vieuxLyon = list(set(zip(df['lat'], df['long'], df['dbscan_cluster'])))
dm.generate_map(coordinates_vieuxLyon, 5000, './maps/mapFinalClustering.html')



