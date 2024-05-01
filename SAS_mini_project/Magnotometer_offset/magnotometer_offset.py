from sklearn.covariance import MinCovDet
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.spatial.distance import euclidean

def find_enclosing_circle(points):
    hull = ConvexHull(points)
    center = np.mean(points[hull.vertices], axis=0)

    radius = max([euclidean(center, point) for point in points[hull.vertices]])

    return center, radius

# Replace 'filename.txt' with the path to your CSV file
filename = '/Users/jakob/Documents/gits/HVACControl/SAS_mini_project/Magnotometer_offset/magnoOffset.txt'

column_names = ['X', 'Y', 'Z']

# Read the CSV file into a DataFrame
data = pd.read_csv(filename,names=column_names)
# Assuming 'data' is your dataset where data[:,0] represents x-coordinates and data[:,1] represents y-coordinates


fig, ax = plt.subplots()
ax.scatter(data['X'],data['Y'])
ax.scatter(data['X'],data['Z'])
ax.scatter(data['Y'],data['Z'])
ax.axis('equal')


# Fit Minimum Covariance Determinant estimator
center, radius = find_enclosing_circle(data[['X','Y']].values)

circle = plt.Circle(center, radius, color='r', fill=False, label='Enclosing Circle')
ax.add_artist(circle)

plt.show