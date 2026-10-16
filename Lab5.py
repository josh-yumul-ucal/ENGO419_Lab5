import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
import pandas as pd

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

# Check that I uploaded the right files with the right names hopefully
assert xhat.shape == (5, 2)
assert Cxhat.shape == (10, 10)

# Assigning coordinates to one array 
coords = np.zeros((7, 2))
for k in range(5):
    coords[UNKNOWN_IDS[k] - 1] = xhat[k]
for row in revised_coords:
    coords[int(row[0]) - 1] = row[1:3]

def covariance_block(first_point, second_point):
    # If point 2 or 4, variance = 0 because they are control points
    if first_point not in UNKNOWN_IDS or second_point not in UNKNOWN_IDS:
        return np.zeros((2,2))

    # Multiply by two because Cx stores each point in a coordinate pair as a separate column
    # i.e. X1 Y1 X2 Y2
    row_start = 2 * UNKNOWN_IDS.index(first_point)
    col_start = 2 * UNKNOWN_IDS.index(second_point)

    return Cxhat[row_start:row_start + 2, col_start:col_start + 2]

def ellipse(C):
    # Takes C: 2x2 covariance matrix result from "covariance_block" function
    sx2 = C[0,0] # var x
    sy2 = C[1,1] # var y
    sxy = C[0,1] # cov xy

    root = np.sqrt(((sx2 - sy2) / 2) ** 2 + sxy ** 2)
    # Semi-axes (Check slide 4.21 of Sideris notes)
    a = np.sqrt((sx2 + sy2) / 2 + root)
    b = np.sqrt((sx2 + sy2) / 2 - root)
    phi = np.degrees(0.5 * np.arctan2(2 * sxy, sx2 - sy2))

    # a and b are the semi-axes of the error ellipse
    # phi is the angle from the x-axis to a
    return a, b, phi

# Sideris slides 4.24
# Computing expansion factor using confidence
expansion_factor = np.sqrt(chi2.ppf(CONFIDENCE, 2))

station = []
for point in UNKNOWN_IDS:
    a, b, phi = ellipse(covariance_block(point, point))
    X, Y = coords[point - 1]

    # appends to stations array: point index, X-coordinate, Y-coordinate,
    # a and b converted to [mm], phi, a and b converted to [mm] and scaled by expansion factor
    station.append([point, X, Y, a * 1000, b * 1000, phi, expansion_factor * a * 1000, expansion_factor * b * 1000])
station = np.array(station)

relative = []
for row in distances:
    i = int(row[0])
    j = int(row[1])

    C_deltaij = covariance_block(i,i) + covariance_block(j, j) - covariance_block(i, j) - covariance_block(j, i)

    a, b, phi = ellipse(C_deltaij)
    X, Y - (coords[i - 1] + coords[j -1]) / 2
    relative.append([i, j, X, Y, a * 1000, b * 1000, phi, expansion_factor * a * 1000, expansion_factor * b * 1000])
relative = np.array(relative)

headers = ["Point", "X(m)", "Y(m)", "a(mm)", "b(mm)", "phi(deg)", "a95(mm)", "b95(mm)"]

print(f"95% Expansion Factor: {expansion_factor}")
print(f"Station error ellipses")

# Using pandas to print results to terminal

df = pd.DataFrame(station, columns=headers)
df["Point"] = df["Point"].astype(int)

print(df.to_string(index=False))
