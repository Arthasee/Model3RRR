"""test for a 3rrr class"""

import numpy as np
from numpy import pi, array, cos, sin, atan2, sqrt, acos
import matplotlib.pyplot as plt
import pygame
from singularity import *
import pygame.locals

# from trace_rob import trace_rob, trace_rob_game
# from mgi_analytique import mgi_analytique


class Robot3RRR:
    """class of the robot 3RRR"""
    def __init__(self, l1=0.13, l2=0.15, rb=0.164, re=0.04618):
        self.clock = [0.0]
        self.l1 = l1
        self.l2 = l2
        self.rb = rb
        self.re = re
        self.pos_eff = [0., 0., 0.]
        self.pos = []
        self.q = [0, pi/2, 0, pi/2, 0, pi/2]
        self.game = False
        self.step = 0.1
        self.dimension = (1, 1)
        self.game_dimensions = (1024, 780)
        self.scale = self.game_dimensions[0]/self.dimension[0]
        self.fps = 60
        self.pen = True
        self.interpolate = False

    def __str__(self):
        return f"Robot(l1 = {self.l1}, l2 = {self.l2}, rb = {self.rb}, re = {self.re})"

    def __repr__(self):
        return str(self)

    def mgi_analytique(self, eff):
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
            th = array([[rot[0][0], rot[0][1], self.rb*cos(ang2[i])],
                        [rot[1][0], rot[1][1], self.rb*sin(ang2[i])],
                        [0, 0, 1]])

            pei_e = array([self.re*cos(ang2[i]), self.re*sin(ang2[i]), 1])
            pei_0 = th_eff.dot(pei_e)

            pei_i = np.linalg.inv(th).dot(pei_0)

            x = pei_i[0]
            y = pei_i[1]

            aux = (x**2+y**2-self.l1**2-self.l2**2)/(2*self.l1*self.l2)
            if abs(aux) <= 1:
                beta = acos(aux)
            else:
                beta = 0
                print("[ERREUR] -- problème d'atteignabilité")
                return 0
            alpha = atan2(y, x) - atan2(self.l2*sin(beta), self.l1+self.l2*cos(beta))
            q = np.append(q, alpha)
            q = np.append(q, beta)
        print(q)
        return q

    def trace_rob(self, q, name):
        """trace the robot with matplotlib.pyplot

        Args:
            q (list): angle values of the 3 arms
            name (int or str): the name (or number) of the figure to differentiate\
            methods

        Returns:
            matplot.pyplot.figure: the figure with the robot
        """
        alpha1 = q[0]
        beta1 = q[1]
        alpha2 = q[2]
        beta2 = q[3]
        alpha3 = q[4]
        beta3 = q[5]

        rot1 = array([[cos(2*pi/3), -sin(2*pi/3)], [sin(2*pi/3), cos(2*pi/3)]])
        rot2 = array([[cos(4*pi/3), -sin(4*pi/3)], [sin(4*pi/3), cos(4*pi/3)]])

        p10 = array([0, -self.rb])
        first_row1 = array([[1, 0, 0], [0, 1, -self.rb], [0, 0, 1]])
        p11 = first_row1.dot(array([self.l1*cos(alpha1), self.l1*sin(alpha1), 1]))
        p12 = first_row1.dot(array([self.l1*cos(alpha1)+self.l2*cos(alpha1+beta1),
                                    self.l1*sin(alpha1)+self.l2*sin(alpha1+beta1),
                                    1]))

        p20 = array([self.rb*sqrt(3)/2, self.rb/2])
        first_row2 = array([[rot1[0][0], rot1[0][1], p20[0]],
                            [rot1[1][0], rot1[1][1], p20[1]]])
        p21 = array([first_row2[0],
                    first_row2[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(alpha2), self.l1*sin(alpha2), 1]))
        p22 = array([first_row2[0],
                    first_row2[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(alpha2)+self.l2*cos(alpha2+beta2),
                                            self.l1*sin(alpha2)+self.l2*sin(alpha2+beta2),
                                            1]))

        p30 = array([-self.rb*sqrt(3)/2, self.rb/2])
        first_row3 = array([[rot2[0][0], rot2[0][1], p30[0]],
                            [rot2[1][0], rot2[1][1], p30[1]]])
        p31 = array([first_row3[0],
                    first_row3[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(alpha3), self.l1*sin(alpha3), 1]))
        p32 = array([first_row3[0],
                    first_row3[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(alpha3)+self.l2*cos(alpha3+beta3),
                                            self.l1*sin(alpha3)+self.l2*sin(alpha3+beta3),
                                            1]))

        f = plt.figure(name)
        plt.plot([p10[0], p11[0], p12[0]], [p10[1], p11[1], p12[1]])
        plt.plot([p20[0], p21[0], p22[0]], [p20[1], p21[1], p22[1]])
        plt.plot([p30[0], p31[0], p32[0]], [p30[1], p31[1], p32[1]])
        plt.plot([p12[0], p22[0], p32[0], p12[0]],
                [p12[1], p22[1], p32[1], p12[1]], linewidth=2)
        plt.axis("square")
        plt.axis("equal")
        # plt.show()
        return f

    def trace_rob_game(self, q):
        """trace the robot with pygame

        Args:
            q (list): angle values of the 3 arms

        Returns:
            pygame.draw: the figure with the robot
        """
        alpha1 = q[0]
        beta1 = q[1]
        alpha2 = q[2]
        beta2 = q[3]
        alpha3 = q[4]
        beta3 = q[5]

        rot1 = array([[cos(2*pi/3), -sin(2*pi/3)], [sin(2*pi/3), cos(2*pi/3)]])
        rot2 = array([[cos(4*pi/3), -sin(4*pi/3)], [sin(4*pi/3), cos(4*pi/3)]])

        p10 = array([0, -self.rb])
        first_row1 = array([[1, 0, 0], [0, 1, -self.rb], [0, 0, 1]])
        p11 = first_row1.dot(array([self.l1*cos(alpha1), self.l1*sin(alpha1), 1]))
        p12 = first_row1.dot(array([self.l1*cos(alpha1)+self.l2*cos(alpha1+beta1),
                                    self.l1*sin(alpha1)+self.l2*sin(alpha1+beta1),
                                    1]))

        p20 = array([self.rb*sqrt(3)/2, self.rb/2])
        first_row2 = array([[rot1[0][0], rot1[0][1], p20[0]],
                            [rot1[1][0], rot1[1][1], p20[1]]])
        p21 = array([first_row2[0],
                    first_row2[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(alpha2), self.l1*sin(alpha2), 1]))
        p22 = array([first_row2[0],
                    first_row2[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(alpha2)+self.l2*cos(alpha2+beta2),
                                            self.l1*sin(alpha2)+self.l2*sin(alpha2+beta2),
                                            1]))

        p30 = array([-self.rb*sqrt(3)/2, self.rb/2])
        first_row3 = array([[rot2[0][0], rot2[0][1], p30[0]],
                            [rot2[1][0], rot2[1][1], p30[1]]])
        p31 = array([first_row3[0],
                    first_row3[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(alpha3), self.l1*sin(alpha3), 1]))
        p32 = array([first_row3[0],
                    first_row3[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(alpha3)+self.l2*cos(alpha3+beta3),
                                            self.l1*sin(alpha3)+self.l2*sin(alpha3+beta3),
                                            1]))

        gamma1 = atan2(p12[1]-p11[1], p12[0] - p11[0])
        gamma2 = atan2(p22[1]-p21[1], p22[0] - p21[0])
        gamma3 = atan2(p32[1]-p31[1], p32[0] - p31[0])
        
        np12 = np.array([p12[0], p12[1], 0])
        np10 = np.array([p10[0], p10[1], 0])
        np22 = np.array([p22[0], p22[1], 0])
        np20 = np.array([p20[0], p20[1], 0])
        np32 = np.array([p32[0], p32[1], 0])
        np30 = np.array([p30[0], p30[1], 0])
        
        
        d1 = (self.pos_eff-p12).dot(array([-sin(gamma1),cos(gamma1),1]))
        d2 = (self.pos_eff-p22).dot(array([-sin(gamma2),cos(gamma2),1]))
        d3 = (self.pos_eff-p32).dot(array([-sin(gamma3),cos(gamma3),1]))
        
        e1 = np.linalg.norm((p11-np10)*(np12-np10)/np.linalg.norm(np12-np10))
        e2 = np.linalg.norm((p21-np20)*(np22-np20)/np.linalg.norm(np22-np20))
        e3 = np.linalg.norm((p31-np30)*(np32-np30)/np.linalg.norm(np32-np30))

        detA = det_A(gamma1, gamma2, gamma3, d1, d2, d3)
        detB = det_B(e1, e2, e3)
        
        if detA == 0:
            if gamma1/pi == gamma2/pi and gamma2/pi == gamma3/pi:
                print(f"Singularité parallèle, les trois droites sont parallèles.")
            else:
                print(f"Singularité parallèle, les trois droites sont concourantes")
        if detB == 0:
            print(f"Singularité série, le bras 3 est à la limite de son espace de travail")

        return p10, p11, p12, p20, p21, p22, p30, p31, p32

    def draw(self, screen=None):
        """draw the robot with matplotlib or pygame

        Args:
            screen (pygame.display, optional): the screen of pygame if used.\
                Defaults to None.
        """
        if not self.game:
            self.trace_rob(self.q, 1)
            plt.show()
            return

        q = self.q
        offset2 = array([self.game_dimensions[0], self.game_dimensions[1]])
        offset3 = array([self.game_dimensions[0],
                        self.game_dimensions[1],
                        0])

        p10, p11, p12, p20, p21, p22, p30, p31, p32 = self.trace_rob_game(q)

        p10 *= self.scale
        p10 += offset2/2

        p11 *= self.scale
        p11 += offset3/2

        p12 *= self.scale
        p12 += offset3/2

        p20 *= self.scale
        p20 += offset2/2

        p21 *= self.scale
        p21 += offset3/2

        p22 *= self.scale
        p22 += offset3/2

        p30 *= self.scale
        p30 += offset2/2

        p31 *= self.scale
        p31 += offset3/2

        p32 *= self.scale
        p32 += offset3/2

        l1 = pygame.draw.line(screen, (255, 0, 0),
                              (p10[0], p10[1]), (p11[0], p11[1]), 2)
        l2 = pygame.draw.line(screen, (255, 0, 255),
                              (p11[0], p11[1]), (p12[0], p12[1]), 2)

        l3 = pygame.draw.line(screen, (255, 0, 0),
                              (p20[0], p20[1]), (p21[0], p21[1]), 2)
        l4 = pygame.draw.line(screen, (255, 0, 255),
                              (p21[0], p21[1]), (p22[0], p22[1]), 2)

        l5 = pygame.draw.line(screen, (255, 0, 0),
                              (p30[0], p30[1]), (p31[0], p31[1]), 2)
        l6 = pygame.draw.line(screen, (255, 0, 255),
                              (p31[0], p31[1]), (p32[0], p32[1]), 2)

        triangle = pygame.draw.polygon(screen,
                                       (0, 255, 0),
                                       [(p12[0], p12[1]),
                                        (p22[0], p22[1]),
                                        (p32[0], p32[1])])
        
        # Croix au centre du triangle
        cx = (p12[0] + p22[0] + p32[0]) / 3
        cy = (p12[1] + p22[1] + p32[1]) / 3
        size = 3
        pygame.draw.line(screen, (0, 0, 0), (cx - size, cy - size), (cx + size, cy + size), 2)
        pygame.draw.line(screen, (0, 0, 0), (cx - size, cy + size), (cx + size, cy - size), 2)
        
        # Traçage de trajectoire
        if len(self.pos) > 1 and not self.interpolate:
            for i in range(len(self.pos) - 1):
                # p1 = array(self.pos[i][:2]) * self.scale + offset2 / 2
                p2 = array(self.pos[i + 1][:2]) * self.scale + offset2 / 2
                pygame.draw.circle(screen, (0, 0, 255),(p2[0], p2[1]), 1,0)
        elif self.interpolate:
            for i in range(len(self.pos) - 1):
                p1 = array(self.pos[i][:2]) * self.scale + offset2 / 2
                p2 = array(self.pos[i + 1][:2]) * self.scale + offset2 / 2
                pygame.draw.line(screen, (0, 0, 255),(p1[0], p1[1]),(p2[0], p2[1]), 2)

    def simulate(self):
        """simulate on pygame the robot and its displacements"""
        if not self.game:
            return
        pygame.init()
        screen = pygame.display.set_mode(self.game_dimensions)
        clock = pygame.time.Clock()
        # font = pygame.font.Font(None, 36)

        running = True

        while running:
            clock.tick(self.fps)
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            screen.fill((255, 255, 255))

            new_pos_eff = self.pos_eff[:]

            if keys[pygame.K_s]:
                new_pos_eff[1] += 0.001
                new_pos_eff[1] = min(1, new_pos_eff[1])
            elif keys[pygame.K_z]:
                new_pos_eff[1] -= 0.001
                new_pos_eff[1] = max(-1, new_pos_eff[1])
            elif keys[pygame.K_q]:
                new_pos_eff[0] -= 0.001
                new_pos_eff[0] = max(-1, new_pos_eff[0])
            elif keys[pygame.K_d]:
                new_pos_eff[0] += 0.001
                new_pos_eff[0] = min(1, new_pos_eff[0])
            elif keys[pygame.K_e]:
                new_pos_eff[2] += 0.01
                new_pos_eff[2] = min(1, new_pos_eff[2])
            elif keys[pygame.K_a]:
                new_pos_eff[2] -= 0.01
                new_pos_eff[2] = max(-1, new_pos_eff[2])
            elif keys[pygame.K_t]:
                self.pen = not self.pen

            new_q = self.mgi_analytique(new_pos_eff)

            if not isinstance(new_q, int):  # if q == 0
                self.pos_eff = new_pos_eff
                self.q = new_q
                if self.pen:
                    self.pos.append(self.pos_eff[:])  # trace que si valide

            self.clock.append(self.clock[-1] + self.step)
            self.draw(screen)
            pygame.display.flip()

            if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
                running = False
                pygame.quit()
                return "fin"
            
    def interpolate_path(self, points, n_steps=50, fps = 30):
        self.interpolate = True
        self.fps = fps  

        if not self.game:
            return
        pygame.init()
        screen = pygame.display.set_mode(self.game_dimensions)
        clock = pygame.time.Clock()

        running = True
        while running:
            for i in range(len(points) - 1):
                pygame.event.pump()
                keys = pygame.key.get_pressed()

                p_start = np.array(points[i])
                p_end = np.array(points[i + 1])
                for t in np.linspace(0, 1, n_steps):
                    
                    if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
                        running = False
                        pygame.quit()
                        return "fin"

                    p_interp = (1 - t) * p_start + t * p_end
                    
                    new_q = self.mgi_analytique(p_interp)

                    if not isinstance(new_q, int):  # if q == 0
                        self.pos_eff = p_interp
                        self.q = new_q
                        if self.pen:
                            self.pos.append(self.pos_eff[:])  # trace que si valide
                    
                    screen.fill((255, 255, 255))
                    clock.tick(self.fps)
                    self.clock.append(self.clock[-1] + self.step)
                    self.draw(screen)
                    pygame.display.flip()

    
        self.interpolate = False
        self.fps = 60

    def trace_square(self, height = 0.07, n_steps = 100, fps = 60):
        """Trace un carré"""

        square_points = [
            [-height, -height, 0],
            [ height, -height, 0],
            [ height,  height, 0],
            [-height,  height, 0],
            [-height, -height, 0],  # retour au début
        ]

        self.pos = []
        self.pen = True

        self.interpolate_path(square_points, n_steps = n_steps, fps = fps)

    def trace_circle(self, center = (0.0, 0.0), radius=0.07, N = 100, n_steps = 10, fps = 60):
        """Trace un cercle"""

        circle_points = []
        angles = np.linspace(0, 2 * pi, N)

        for angle in angles:
            # Calcul de la position cible sur le cercle
            x = center[0] + radius * cos(angle)
            y = center[1] + radius * sin(angle)
            circle_points.append([x, y, 0])

        self.interpolate_path(circle_points, n_steps = n_steps, fps = fps)

if __name__ == '__main__':

    test_control = 1
    test_square = 0
    test_circle = 0

    robot = Robot3RRR()

    if test_control:
        robot.game = True
        robot.q = robot.mgi_analytique(robot.pos_eff)
        robot.simulate()
        robot.game = False
        robot.draw()

    if test_square:
        robot.game = True
        robot.trace_square()    #Rester appuyé sur échap pour quitter

    elif test_circle:
        robot.game = True
        robot.trace_circle()    #Rester appuyé sur échap pour quitter