"""test for a 3rrr class"""

from numpy import pi, sin, cos, array, sqrt
import matplotlib.pyplot as plt
import pygame
import pygame.locals

from trace_rob import trace_rob
from mgi_analytique import mgi_analytique


class Robot3RRR:
    def __init__(self, l1=0.1, l2=0.1, rb=0.1322594, re=0.07):
        self.clock = [0.0]
        self.l1 = l1
        self.l2 = l2
        self.rb = rb
        self.re = re
        self.pos_eff = [0., 0., 0.]
        self.q = [0, pi/2, 0, pi/2, 0, pi/2]
        self.game = False
        self.step = 0.1
        self.dimension = (40, 40)
        self.game_dimensions = (1024, 780)
        self.scale = self.game_dimensions[0]/self.dimension[0]
        self.fps = 60

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def draw(self, screen=None):
        if not self.game:
            f = trace_rob(self.q, 1)
            plt.show()
            return
        rot1 = array([[cos(2*pi/3), -sin(2*pi/3)], [sin(2*pi/3), cos(2*pi/3)]])
        rot2 = array([[cos(4*pi/3), -sin(4*pi/3)], [sin(4*pi/3), cos(4*pi/3)]])

        p10 = array([0, -self.rb])*self.scale
        p10 += array([self.dimension[0], self.dimension[1]])/2

        first_row1 = array([[1, 0, 0], [0, 1, -self.rb], [0, 0, 1]])
        p11 = first_row1.dot(array([self.l1*cos(self.q[0]),
                                    self.l1*sin(self.q[0]),
                                    1]))*self.scale

        p11 += array([self.dimension[0], self.dimension[1], 0])/2

        p12 = first_row1.dot(array([self.l1*cos(self.q[0])+self.l2*cos(self.q[0]+self.q[1]),
                                    self.l1*sin(self.q[0])+self.l2*sin(self.q[0]+self.q[1]),
                                    1]))*self.scale
        p12 += array([self.dimension[0], self.dimension[1], 0])/2

        p20 = array([self.rb*sqrt(3)/2, self.rb/2])*self.scale
        p20 += array([self.dimension[0], self.dimension[1]])/2

        first_row2 = array([[rot1[0][0], rot1[0][1], p20[0]],
                            [rot1[1][0], rot1[1][1], p20[1]]])
        p21 = array([first_row2[0],
                    first_row2[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(self.q[3]),
                                           self.l1*sin(self.q[3]),
                                           1]))*self.scale
        p21 += array([self.dimension[0], self.dimension[1], 0])/2

        p22 = array([first_row2[0],
                    first_row2[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(self.q[3])+self.l2*cos(self.q[3]+self.q[3]),
                                            self.l1*sin(self.q[3])+self.l2*sin(self.q[3]+self.q[3]),
                                            1]))*self.scale
        p22 += array([self.dimension[0], self.dimension[1], 0])/2

        p30 = array([-self.rb*sqrt(3)/2, self.rb/2])*self.scale
        p30 += array([self.dimension[0], self.dimension[1]])/2

        first_row3 = array([[rot2[0][0], rot2[0][1], p30[0]],
                            [rot2[1][0], rot2[1][1], p30[1]]])
        p31 = array([first_row3[0],
                    first_row3[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(self.q[3]),
                                           self.l1*sin(self.q[3]),
                                           1]))*self.scale
        p31 += array([self.dimension[0], self.dimension[1], 0])/2

        p32 = array([first_row3[0],
                    first_row3[1],
                    [0, 0, 1]]).dot(array([self.l1*cos(self.q[3])+self.l2*cos(self.q[3]+self.q[5]),
                                            self.l1*sin(self.q[3])+self.l2*sin(self.q[3]+self.q[5]),
                                            1]))*self.scale
        p32 += array([self.dimension[0], self.dimension[1], 0])/2

        l1 = pygame.draw.line(screen, (255, 0, 0), (p10[0], p10[1]), (p11[0], p11[1]), 2)
        l2 = pygame.draw.line(screen, (255, 0, 255), (p11[0], p11[1]), (p12[0], p12[1]), 2)

        l3 = pygame.draw.line(screen, (255, 0, 0), (p20[0], p20[1]), (p21[0], p21[1]), 2)
        l4 = pygame.draw.line(screen, (255, 0, 255), (p21[0], p21[1]), (p22[0], p22[1]), 2)

        l5 = pygame.draw.line(screen, (255, 0, 0), (p30[0], p30[1]), (p31[0], p31[1]), 2)
        l6 = pygame.draw.line(screen, (255, 0, 255), (p31[0], p31[1]), (p32[0], p32[1]), 2)

        triangle = pygame.draw.polygon(screen, (0, 255, 0), [(p12[0], p12[1]),
                                                             (p22[0], p22[1]),
                                                             (p32[0], p32[1])])

        # return (l1, l2, l3, l4, l5, l6, triangle)

    def simulate(self):
        if not self.game:
            return
        successes, failures = pygame.init()
        screen = pygame.display.set_mode(self.game_dimensions)
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)

        running = True

        while running:
            clock.tick(self.fps)
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            screen.fill((255, 255, 255))
            self.draw(screen)

            time_text = font.render(f"Time: {round(self.clock[-1], 1)}", True, (0, 0, 0))
            text_rect = time_text.get_rect(bottomright=(self.game_dimensions[0] - 10, self.game_dimensions[1] - 10))
            screen.blit(time_text, text_rect)

            pygame.display.flip()

            if keys[pygame.K_ESCAPE]:
                self.running = False
                pygame.quit()


if __name__ == '__main__':
    robot = Robot3RRR()
    robot.game = True
    robot.q = mgi_analytique(robot.pos_eff)
    robot.simulate()
