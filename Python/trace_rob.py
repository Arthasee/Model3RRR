""" trace robot code """

from numpy import cos, sin, pi, array, sqrt
import numpy as np
import matplotlib.pyplot as plt

L1 = 0.10
L2 = 0.10
RB = 0.1322594
RE = 0.07

def trace_rob(q, name):
    alpha1 = q[0]
    beta1 = q[1]
    alpha2 = q[2]
    beta2 = q[3]
    alpha3 = q[4]
    beta3 = q[5]

    Rot1 = array([[cos(2*pi/3), -sin(2*pi/3)], [sin(2*pi/3), cos(2*pi/3)]])
    Rot2 = array([[cos(4*pi/3), -sin(4*pi/3)], [sin(4*pi/3), cos(4*pi/3)]])

    p10 = array([0, -RB])
    first_row1 = array([[1, 0, 0], [0, 1, -RB], [0, 0, 1]])
    p11 = first_row1.dot(array([L1*cos(alpha1), L1*sin(alpha1), 1]))
    p12 = first_row1.dot(array([L1*cos(alpha1)+L2*cos(alpha1+beta1), L1*sin(alpha1)+L2*sin(alpha1+beta1), 1]))

    p20 = array([RB*sqrt(3)/2, RB/2])
    first_row2 = array([[Rot1[0][0], Rot1[0][1], p20[0]], [Rot1[1][0], Rot1[1][1], p20[1]]])
    p21 = array([first_row2[0], first_row2[1], [0, 0, 1]]).dot(array([L1*cos(alpha2), L1*sin(alpha2), 1]))
    p22 = array([first_row2[0], first_row2[1], [0, 0, 1]]).dot(array([L1*cos(alpha2)+L2*cos(alpha2+beta2), L1*sin(alpha2)+L2*sin(alpha2+beta2), 1]))

    p30 = array([-RB*sqrt(3)/2, RB/2])
    first_row3 = array([[Rot2[0][0], Rot2[0][1], p30[0]], [Rot2[1][0], Rot2[1][1], p30[1]]])
    p31 = array([first_row3[0], first_row3[1], [0, 0, 1]]).dot(array([L1*cos(alpha3), L1*sin(alpha3), 1]))
    p32 = array([first_row3[0], first_row3[1], [0, 0, 1]]).dot(array([L1*cos(alpha3)+L2*cos(alpha3+beta3), L1*sin(alpha3)+L2*sin(alpha3+beta3), 1]))

    f = plt.figure(name)
    plt.plot([p10[0], p11[0], p12[0]], [p10[1], p11[1], p12[1]])
    plt.plot([p20[0], p21[0], p22[0]], [p20[1], p21[1], p22[1]])
    plt.plot([p30[0], p31[0], p32[0]], [p30[1], p31[1], p32[1]])
    plt.plot([p12[0], p22[0], p32[0], p12[0]], [p12[1], p22[1], p32[1], p12[1]], linewidth=2)
    plt.axis("square")
    plt.axis("equal")
    # plt.show()
    return f

