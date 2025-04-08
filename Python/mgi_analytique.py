"""mgi analytic code"""

from numpy import pi, array, cos, sin, acos, atan2
import numpy as np

L1 = 0.10
L2 = 0.10
RB = 0.1322594
RE = 0.07


def mgi_analytique(eff):
    """determine the inverse geometric model

    Args:
        eff (list): position of the effectors

    Returns:
        list: angles of the arms
    """
    rot_eff = array([[cos(eff[2]), -sin(eff[2])], [sin(eff[2]), cos(eff[2])]])
    transl = array([eff[0], eff[1]])
    th_eff = array([[rot_eff[0][0], rot_eff[0][1], transl[0]],
                    [rot_eff[1][0], rot_eff[1][1], transl[1]],
                    [0, 0, 1]])

    ang1 = array([0, 2*pi/3, 4*pi/3])

    ang2 = array([-pi/2, pi/6, 5*pi/6])

    q = array([])

    for i in range(3):
        rot = array([[cos(ang1[i]), -sin(ang1[i])],
                     [sin(ang1[i]), cos(ang1[i])]])
        th = array([[rot[0][0], rot[0][1], RB*cos(ang2[i])],
                    [rot[1][0], rot[1][1], RB*sin(ang2[i])],
                    [0, 0, 1]])

        pei_e = array([RE*cos(ang2[i]), RE*sin(ang2[i]), 1])
        pei_0 = th_eff.dot(pei_e)

        pei_i = np.linalg.inv(th).dot(pei_0)

        x = pei_i[0]
        y = pei_i[1]

        aux = (x**2+y**2-L1**2-L2**2)/(2*L1*L2)
        if abs(aux) < 1:
            beta = acos(aux)
        else:
            beta = 0
            print("[ERREUR] -- problème d'atteignabilité")
        alpha = atan2(y, x) - atan2(L2*sin(beta), L1+L2*cos(beta))
        q = np.append(q, alpha)
        q = np.append(q, beta)
    print(q)
    return q
