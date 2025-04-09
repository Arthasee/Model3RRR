"""test for a 3rrr class"""

from numpy import pi, sin, cos, array, sqrt
import matplotlib.pyplot as plt
import pygame
import pygame.locals

from trace_rob import trace_rob, trace_rob_game
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
        self.dimension = (1, 1)
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

        p10, p11, p12, p20, p21, p22, p30, p31, p32 = trace_rob_game(self.q)

        p10 *= self.scale
        p10 += array([self.game_dimensions[0], self.game_dimensions[1]])/2

        p11 *= self.scale
        p11 += array([self.game_dimensions[0], self.game_dimensions[1], 0])/2

        p12 *= self.scale
        p12 += array([self.game_dimensions[0], self.game_dimensions[1], 0])/2

        p20 *= self.scale
        p20 += array([self.game_dimensions[0], self.game_dimensions[1]])/2

        p21 *= self.scale
        p21 += array([self.game_dimensions[0], self.game_dimensions[1], 0])/2

        p22 *= self.scale
        p22 += array([self.game_dimensions[0], self.game_dimensions[1], 0])/2

        p30 *= self.scale
        p30 += array([self.game_dimensions[0], self.game_dimensions[1]])/2

        p31 *= self.scale
        p31 += array([self.game_dimensions[0], self.game_dimensions[1], 0])/2

        p32 *= self.scale
        p32 += array([self.game_dimensions[0], self.game_dimensions[1], 0])/2

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
