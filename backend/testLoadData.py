import numpy as np
print("loading state data")
statesAndCenters   = np.loadtxt("stateData/stateCenters.txt",dtype = str,delimiter  = ":",usecols  = (0,2))
states             = statesAndCenters[:,0]
centers = []
for i,center in enumerate(statesAndCenters[:,1]):
    coords = center.split(' ')
    coords[0] = float(coords[0])
    coords[1] = float(coords[1])
    centers.append(coords)
import numpy as np
centers = np.array(centers)
statesAndMoods = dict(zip(states, np.transpose([[0] * len(states),[1] * len(states),centers[:,0],centers[:,1]] ) ))
print statesAndMoods