"""robot visualization using urdf"""

from urdfpy import URDF

robot = URDF.load('pkg/urdf/robot.urdf')
robot.show()
