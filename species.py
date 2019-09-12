import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_species_distributions
from sklearn.datasets.species_distributions import construct_grids
from sklearn.neighbors import KernelDensity
import pandas as pd

vba = pd.read_excel('VBA_data.xls') # VBA (training data)

# if basemap is available, we'll use it.
# otherwise, we'll improvise later...
try:
    from mpl_toolkits.basemap import Basemap
    basemap = True
except ImportError:
    basemap = False

# Get matrices/arrays of species IDs and locations
data = fetch_species_distributions()
species_names = ['Bradypus Variegatus', 'Microryzomys Minutus']
# The only attributes we care about in `training` are lat and long.
Xtrain = np.vstack([data['train']['dd lat'],
                    data['train']['dd long']]).T


# Microryzomys Minutus gets coded as 1,
# Bradypus Variegatus as 0
ytrain = np.array([d.decode('ascii').startswith('micro')
                  for d in data['train']['species']], dtype='int')


Xtrain *= np.pi / 180.  # Convert lat/long to radians

print(data)

# Set up the data grid for the contour plot
xgrid, ygrid = construct_grids(data)
# To help kernel density estimation take a reasonable length of time we
# consistently use every 5th data point
X, Y = np.meshgrid(xgrid[::5], ygrid[::5][::-1])
# We'll make use of the fact that coverages[6] has measurements at all
# land points.  This will help us decide between land and water.
land_reference = data.coverages[6][::5, ::5]
# -9999 means water.  Make a Boolean grid identifying land.
land_mask = (land_reference > -9999).ravel()

xy = np.vstack([Y.ravel(), X.ravel()]).T
xy = xy[land_mask]
xy *= np.pi / 180.

ois = [(i,cls) for (i,cls) in enumerate(ytrain) if cls == 1]
zis = [(i,cls) for (i,cls) in enumerate(ytrain) if cls == 0]

# Plot map of South America with distributions of each species
fig = plt.figure()
fig.subplots_adjust(left=0.05, right=0.95, wspace=0.05)

for i in range(2):
    plt.subplot(1, 2, i + 1)

    # construct a kernel density estimate of the distribution
    print(" - computing KDE in spherical coordinates")
    kde = KernelDensity(bandwidth=0.04, metric='haversine',
                        kernel='gaussian', algorithm='ball_tree')
    kde.fit(Xtrain[ytrain == i])

    # evaluate only on the land: -9999 indicates ocean
    Z = -9999 + np.zeros(land_mask.shape[0])
    Z[land_mask] = np.exp(kde.score_samples(xy))
    Z = Z.reshape(X.shape)

    # plot contours of the density
    levels = np.linspace(0, Z.max(), 25)
    plt.contourf(X, Y, Z, levels=levels, cmap=plt.cm.Reds)
    plt.title(species_names[i])
plt.show()