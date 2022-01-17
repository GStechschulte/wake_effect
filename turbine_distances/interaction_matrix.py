import numpy as np
import pandas as pd
from sklearn.neighbors import DistanceMetric
from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sns

class interaction_matrix():

    def __init__(self, data):

        self.data = data
        
    def calculate_haver(self, tri, plot=bool):

        haversine = DistanceMetric.get_metric('haversine')

        self.data['lat_rad'] = np.radians(self.data['Lat.'])
        self.data['long_rad'] = np.radians(self.data['Long.'])

        # Calculate haversine distances (in meters)
        haversine_distances = haversine.pairwise(self.data[['lat_rad', 'long_rad']].to_numpy())*6373000
        
        if tri == True:
            # Lower triangular matrix
            haversine_triangular = np.tril(haversine_distances)
            # Convert to dataframe
            haversine_df = pd.DataFrame(
                haversine_triangular,
                columns=self.data['WTG'].unique(),
                index=self.data['WTG'].unique()
            )

            subset_proximity_haver = haversine_df[(haversine_df <= 720) & (haversine_df > 250)]
            subset_proximity_haver.fillna(value=0, inplace=True)
            subset_proximity_haver[subset_proximity_haver > 0] = 1
        else:
            # Convert to dataframe
            haversine_df = pd.DataFrame(
                haversine_distances,
                columns=self.data['WTG'].unique(),
                index=self.data['WTG'].unique()
            )

            subset_proximity_haver = haversine_df[(haversine_df <= 1875) & (haversine_df > 625)]
            subset_proximity_haver.fillna(value=0, inplace=True)
            subset_proximity_haver[subset_proximity_haver > 0] = 1

        if plot == True:
            plt.figure(figsize=(12, 8))
            sns.heatmap(subset_proximity_haver)
            #plt.title(self.name)
            plt.show()
        else:
            pass

        return subset_proximity_haver
    
    def calculate_euclidean(self, threshold, tri, plot=bool):

        lat = self.data['Lat.'].values
        long = self.data['Long.'].values

        self.datas = []

        for lat, long in zip(lat, long):
            self.datas.append((lat, long))

        euclid_distances = distance.cdist(self.datas, self.datas, 'euclidean')

        if tri == True:
            euclid_triangular = np.tril(euclid_distances)
            euclid_df = pd.DataFrame(
                euclid_triangular,
                columns=self.data['WTG'].unique(),
                index = self.data['WTG'].unique()
            )

            subset_proximity_euclid = euclid_df[(euclid_df <= threshold) & (euclid_df > 0.0)]
            subset_proximity_euclid.fillna(value=0, inplace=True)
            subset_proximity_euclid[subset_proximity_euclid > 0] = 1
        else:
            euclid_distances = pd.DataFrame(
            distance.cdist(self.datas, self.datas, 'euclidean'), 
            columns=self.data['WTG'].unique(),
            index = self.data['WTG'].unique()
            )

            subset_proximity_euclid = euclid_distances[(euclid_distances <= threshold) & (euclid_distances > 0.0)]
            subset_proximity_euclid.fillna(value=0, inplace=True)
            subset_proximity_euclid[subset_proximity_euclid > 0] = 1

        if plot == True:
            plt.figure(figsize=(12, 8))
            sns.heatmap(subset_proximity_euclid)
            #plt.title(self.name)
            plt.show()
        else:
            pass

        return subset_proximity_euclid