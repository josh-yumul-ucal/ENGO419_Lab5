import numpy as np
import matplotlib.pyplot as plt

xhat = np.loadtxt("final_xhat.txt")
Cxhat = np.loadtxt("final_Cxhat.txt")
revised_coords = np.loadtxt("revised_coords2.txt")

unknown_ids = [1, 3, 5, 6, 7]



C1 = Cxhat[0:2, 0:2]
C3 