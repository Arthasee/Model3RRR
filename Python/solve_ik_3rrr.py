""" solve IK 3RRR robot code"""
from numpy import pi
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

q = sc.optimize.fsolve(solve_eq_nl(q0, pos_eff), q0)

trace_rob(q)

q = mgi_analytique(pos_eff)
trace_rob(q)
