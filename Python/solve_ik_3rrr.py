""" solve IK 3RRR robot code"""
from numpy import pi
import matplotlib.pyplot as plt
import scipy as sc
from solve_eq_nl import solve_eq_nl
from trace_rob import trace_rob
from mgi_analytique import mgi_analytique

L1 = 0.10
L2 = 0.10
RB = 0.1322594
RE = 0.07

pos_eff = [0., 0., 0]

q0 = [0, pi/2, 0, pi/2, 0, pi/2]

q = sc.optimize.fsolve(solve_eq_nl, q0, args=pos_eff)

f1 = trace_rob(q, 1)

qn = mgi_analytique(pos_eff)
f2 = trace_rob(qn, 2)

plt.show()
