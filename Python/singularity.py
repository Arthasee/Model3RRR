import numpy as np

def det_A(g1, g2, g3, d1, d2, d3):

    A = np.zeros((3, 3))
    A[0] = [np.cos(g1), np.sin(g1), d1]
    A[1] = [np.cos(g2), np.sin(g2), d2]
    A[2] = [np.cos(g3), np.sin(g3), d3]

    return np.linalg.det(A)

def B(e1, e2, e3):

    B = np.zeros(3)
    B[0,0] = e1
    B[1,1] = e2
    B[2,2] = e3

    return np.linalg.det(B)

# Singularité parallèle
cte = 0
g1 = cte + np.pi
g2 = cte + 2*np.pi
g3 = cte + 3*np.pi

