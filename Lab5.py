import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

# Using proper pep8 notation now
XHAT_FILE = np.loadtxt("final_xhat.txt")
CXHAT_FILE = np.loadtxt("final_Cxhat.txt")
REVISED_COORDS_FILE = np.loadtxt("revised_coords2.txt")
DISTANCES_FILE = np.loadtxt("distances.txt")

xhat = XHAT_FILE.copy()
Cxhat = CXHAT_FILE.copy()
revised_coords = REVISED_COORDS_FILE.copy()
distances = DISTANCES_FILE.copy()

UNKNOWN_IDS = [1, 3, 5, 6, 7]
CONFIDENCE = 0.95

assert xhat.shape == (5, 2)
assert Cxhat.shape == (10, 10)

# Assigning data to its respective arrays
coords = np.zeros((7, 2))
for k in range(5):
    coords[UNKNOWN_IDS[k] - 1] = xhat[k]
for row in revised_coords:
    coords[row[0] - 1] = row[1:3]

