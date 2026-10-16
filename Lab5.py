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
    X, Y = (coords[i - 1] + coords[j -1]) / 2
    relative.append([i, j, X, Y, a * 1000, b * 1000, phi, expansion_factor * a * 1000, expansion_factor * b * 1000])
relative = np.array(relative)

# Creating print to terminal statements

# Printing station error ellipses and expansion factor
headers = ["Point", "X(m)", "Y(m)", "a(mm)", "b(mm)", "phi(deg)", "a95(mm)", "b95(mm)"]

print(f"95% Expansion Factor: {expansion_factor}")
print(f"Station error ellipses")

df = pd.DataFrame(station, columns=headers)
df["Point"] = df["Point"].astype(int)

print(df.to_string(index=False))


# Printing distance error ellipses
headers = ["Link", "X(m)", "Y(m)", "a(mm)", "b(mm)", "phi(deg)", "a95(mm)", "b95(mm)"]
print("Relative error ellipses")

# Indexes all of relative except for the first two columns which correspond to the points of the distance
df = pd.DataFrame(relative[:, 2:], columns=headers[1:])
# Inserts the first two columns of relative by combining them into one fstring with a dash to show the link
df.insert(0, "Link", [f"{int(r[0])}-{int(r[1])}" for r in relative])
print(df.to_string(index=False))

# End of task 2a)

# Task 2b)
# rewrote the drawEllipse.m script using pyplot
def draw_ellipse(col, a, b, x0, y0, phi):
    phi = np.radians(phi)
    theta = np.linspace(0, 2 * np.pi, 361)

    x = a * np.cos(theta)
    y = b * np.sin(theta)

    X = np.cos(phi) * x - np.sin(phi) * y + x0
    Y = np.sin(phi) * x + np.cos(phi) * y + y0

    plt.plot(X, Y, col, linewidth=2)

# Plot scale so that the ellipses are visible
plot_scale = 3000

plt.figure("Network Plot", figsize=(9, 8))

# Lines for obs dist
for dist in distances:
    i = int(dist[0]) - 1
    j = int(dist[1]) - 1
    plt.plot([coords[i, 0], coords[j, 0]], [coords[i, 1], coords[j, 1]], "k-", linewidth=0.9
    )

# Point labels
plt.scatter(coords[:, 0], coords[:, 1], s=20, zorder=10) 
for i in range(7):
    plt.text(coords[i,0] + 10, coords[i,1] - 25, str(i + 1))

# Scaled ellipses
for s in station:
    draw_ellipse("b", s[6] /1000 * plot_scale, s[7] / 1000 * plot_scale, s[1], s[2], s[5])

# Relative ellipses of observed distances
for r in relative:
    draw_ellipse("r--", r[7] / 1000 * plot_scale, r[8] / 1000 * plot_scale, r[2], r[3], r[6])

plt.plot([], [], "b", label="Station")
plt.plot([], [], "r--", label="Relative")
plt.plot([], [], "k-", label="Distance")
plt.legend()

plt.axis("equal")
plt.grid()
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title(f"Error Ellipses (Scale x{plot_scale})")

plt.savefig("network_ellipses.png")

# Task 2c in report, order of smallest to largest error ellipse below

# Task 2d
station_area = station[:, 6] * station[:, 7]
relative_area = relative[:, 7] * relative[:, 8]
print("Largest relative ellipse:", relative[np.argmax(relative_area), :2])
print("Smallest relative ellipse:", relative[np.argmin(relative_area), :2])
print("Largest station error ellipse: Station", int(station[np.argmax(station_area), 0]))
print("Smallest station error ellipse: Station", int(station[np.argmin(station_area), 0]))


def distance_error(i, j):
    dX, dY = coords[j -1] - coords [i - 1]
    d = np.sqrt(dX**2 + dY**2)

    J = np.array([dX / d, dY / d])

    C_deltaij = covariance_block(i,i) + covariance_block(j, j) - covariance_block(i, j) - covariance_block(j, i)

    sigma_dist = np.sqrt(J @ C_deltaij @ J)

    return d, sigma_dist

# Sort points from smallest to largest station ellipse
order = station[np.argsort(station_area), 0].astype(int)

print("\nTask 2d")
for i, j in [(order[-1], order[-2]), (order[0], order[1])]:
    d, sigma_d = distance_error(i, j)
    print(f"{i}-{j}: {d:.3f} m, σ = {sigma_d*1000:.3f} mm, 1:{d/sigma_d:,.0f}")

plt.show()