"""solve_eq_nl code"""
from numpy import pi, array, cos, sin, zeros
import numpy as np

L1 = 0.10
L2 = 0.10
RB = 0.1322594
RE = 0.07

def solve_eq_nl(q, eff):
    alpha1 = q[0]
    beta1 = q[1]
    alpha2 = q[2]
    beta2 = q[3]
    alpha3 = q[4]
    beta3 = q[5]
    alpha = [alpha1, alpha2, alpha3]
    beta = [beta1, beta2, beta3]

    f = [0, 0, 0, 0, 0, 0]

    ang1 = array([0, 2*pi/3, 4*pi/3])

    ang2 = array([-pi/2, pi/6, 5*pi/6])

    rot_eff = array([[cos(eff[2]), -sin(eff[2])], [sin(eff[2]), cos(eff[2])]])
    transl = array([eff[0], eff[1]])
    # th_eff = array([[[rot_eff], [transl]], [0, 0, 1]])
    th_eff_in = [[rot_eff[0][0], rot_eff[0][1], transl[0]], [rot_eff[1][0], rot_eff[1][1], transl[1]], [0, 0, 1]]
    th_eff = array(th_eff_in)

    for i in range(3):
        pei_e = array([RE*cos(ang2[i]), RE*sin(ang2[i]), 1])

        pei_0 = th_eff.dot(pei_e)

        rot = array([[cos(ang1[i]), -sin(ang1[i])], [sin(ang1[i]), cos(ang1[i])]])
        # thri_0 = array([rot, [RB*cos(ang2[i]), RB*sin(ang2[i])], [0, 0, 1]])
        thri_0 = array([[rot[0][0], rot[0][1], RB*cos(ang2[i])], [rot[1][0], rot[1][1], RB*sin(ang2[i])], [0, 0, 1]])
        pbi = thri_0.dot(array([L1*cos(alpha[i])+L2*cos(alpha[i]+beta[i]), L1*sin(alpha[i])+L2*sin(alpha[i]+beta[i]), 1]))
        if i == 0:
            f[0] = pbi[0] - pei_0[0]
            f[1] = pbi[1] - pei_0[1]
        else:
            f[2*i] = pbi[0] - pei_0[0]
            f[2*i+1] = pbi[1] - pei_0[1]

    return f
 