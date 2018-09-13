import numpy as np


# latf: [latitude] (ndarray)
# longf: [longitude] (ndarray)
# late: [latitude] (ndarray)
# longe: [longitude] (ndarray)
def hubeny(latf, longf, late, longe):
    a = 6378137.0 # GRS80_A
    e2 = 0.00669438002301188 # GRS80_E2
    Mnum = 6335439.327083167 # GRS80_MNUM
    dy = np.radians(late - latf)
    dx = np.radians(longe - longf)
    my = np.radians((latf + late) / 2)
    W = np.sqrt(1 - e2 * np.sin(my)**2)
    M = Mnum / W**3
    N = a / W
    return np.sqrt((dy * M)**2 + (dx * N * np.cos(my))**2)

# points: [[latitude, longitude]] (ndarray)
def sum_distance(points):
    v = np.c_[np.delete(points, -1 , 0), np.delete(points, 0 , 0)]
    return float(np.sum(hubeny(v[:,0], v[:,1], v[:,2], v[:,3])))

def l2_norm(points, compare_point):
    return np.sqrt(np.square(compare_point[0] - points[:,0]) + np.square(compare_point[1] - points[:,1]))
