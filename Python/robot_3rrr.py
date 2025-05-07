"""test for a 3rrr class"""

from numpy import pi, array, cos, sin, tan, sqrt
import matplotlib.pyplot as plt
import pygame
import pygame.locals

# from trace_rob import trace_rob, trace_rob_game
from mgi_analytique import mgi_analytique


class Robot3RRR:
    """class of the robot 3RRR"""
    def __init__(self, l1=0.1, l2=0.1, rb=0.1322594, re=0.07):
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

    def __str__(self):
        return f"Robot(l1 = {self.l1}, l2 = {self.l2}, rb = {self.rb}, re = {self.re})"

    def __repr__(self):
        return str(self)
    
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
        if len(self.pos) > 1 and self.pen:
            for i in range(len(self.pos) - 1):
                # p1 = array(self.pos[i][:2]) * self.scale + offset2 / 2
                p2 = array(self.pos[i + 1][:2]) * self.scale + offset2 / 2
                pygame.draw.circle(screen, (0, 0, 255),(p2[0], p2[1]), 1,0)
                # pygame.draw.line(screen, (0, 0, 255), (p1[0], p1[1]), (p2[0], p2[1]), 2)

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

            new_q = mgi_analytique(new_pos_eff)

            if not isinstance(new_q, int):  # if q == 0
                self.pos_eff = new_pos_eff
                self.q = new_q
                if self.pen:
                    self.pos.append(self.pos_eff[:])  # trace que si valide
                
            self.clock.append(self.clock[-1] + self.step)
            self.draw(screen)
            pygame.display.flip()

            if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
                self.running = False
                pygame.quit()
                return "fin"
            
    def trace_S(self):
        pass


if __name__ == '__main__':
    robot = Robot3RRR()
    robot.game = True
    print(robot)
    robot.q = mgi_analytique(robot.pos_eff)
    robot.simulate()
    robot.game = False
    robot.draw()
