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

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Download required resources
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')



file_path_Lyon = './data/flickr_data2_filtered_clusters.csv'
file_path_VieuxLyon = './data/flickr_data2_largest_cluster_filtered.csv'

# List of files to delete if they exist
files_to_delete = ['./maps/map.html', './elbow_charts/elbow.png', './elbow_charts/distance_to_4th_nearest_point.png', './maps/mapLargestCluster.html', './maps/mapCluster.html', './maps/mapFinalClustering.html']

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

# print number of clusters
print('Number of clusters: ', len(df['dbscan_cluster'].unique()))

# for cluster in df['dbscan_cluster'].unique():
    # df_current_cluster = df[df['dbscan_cluster'] == cluster]

    # # Tokenization
    # tokens = word_tokenize(df_current_cluster['tags'].to_string())
    # # remove punctuation
    # tokens = [word for word in tokens if word.isalnum()]
    # # remove stopwords
    # stop_words_english = set(stopwords.words('english'))
    # tokens = [word for word in tokens if not word in stop_words_english]

    # stop_words_french = set(stopwords.words('french'))
    # tokens = [word for word in tokens if not word in stop_words_french]

    # # remove numbers 
    # tokens = [word for word in tokens if not word.isdigit()]

    # # remove all the words that are not in the english or french dictionary
    # tokens = [word for word in tokens if word.isalpha()]

    # # put all the words in lowercase
    # tokens = [word.lower() for word in tokens]

    # unuseful_words = ['lyon', 'france']
    # tokens = [word for word in tokens if not word in unuseful_words]

    # # remove all words with less than 3 characters
    # tokens = [word for word in tokens if len(word) > 3]


    # # print the most frequent words
    # freq = nltk.FreqDist(tokens)
    # print(f'Most common words in cluster {cluster}: {freq.most_common(1)}')

    # # if there is a word in freqq.most_common(1) add it to df as the name of the cluster
    # if freq.most_common(1):
    #     cluster_name = freq.most_common(1)[0][0]
    #     df.loc[df['dbscan_cluster'] == cluster, 'cluster_name'] = cluster_name
    # else:
    #     df.loc[df['dbscan_cluster'] == cluster, 'cluster_name'] = 'Unknown'
    # # cluster_name = freq.most_common(1)

    # # print(f'Cluster {cluster} is named: {cluster_name[0][0]}')




# # drop all the Unknown clusters
# df = df[df['cluster_name'] != 'Unknown']




# # create coordinates to generate the map
# coordinates_vieuxLyon = list(set(zip(df['lat'], df['long'], df['dbscan_cluster'], df['cluster_name'])))
# dm.generate_map(coordinates_vieuxLyon, 1000, './maps/mapFinalClustering.html')

df_current_cluster = df[df['dbscan_cluster'] == 109]

# Tokenization
tokens = word_tokenize(df_current_cluster['tags'].to_string())
# remove punctuation
tokens = [word for word in tokens if word.isalnum()]
# remove stopwords
stop_words_english = set(stopwords.words('english'))
tokens = [word for word in tokens if not word in stop_words_english]

stop_words_french = set(stopwords.words('french'))
tokens = [word for word in tokens if not word in stop_words_french]

# remove numbers 
tokens = [word for word in tokens if not word.isdigit()]

# remove all the words that are not in the english or french dictionary
tokens = [word for word in tokens if word.isalpha()]

# put all the words in lowercase
tokens = [word.lower() for word in tokens]

unuseful_words = ['lyon', 'france']
tokens = [word for word in tokens if not word in unuseful_words]

# remove all words with less than 3 characters
tokens = [word for word in tokens if len(word) > 3]

print(tokens)


# print the most frequent words
freq = nltk.FreqDist(tokens)
print(f'Most common words in cluster 109: {freq.most_common(1)}')



