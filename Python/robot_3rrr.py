"""test for a 3rrr class"""

from numpy import pi, array
import matplotlib.pyplot as plt
import pygame
import pygame.locals

from trace_rob import trace_rob, trace_rob_game
from mgi_analytique import mgi_analytique


class Robot3RRR:
    """class of the robot 3RRR
    """
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

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def draw(self, screen=None):
        """draw the robot with matplotlib or pygame

        Args:
            screen (pygame.display, optional): the screen of pygame if used.\
                Defaults to None.
        """
        if not self.game:
            trace_rob(self.q, 1)
            plt.show()
            return

        q = self.q
        offset2 = array([self.game_dimensions[0], self.game_dimensions[1]])
        offset3 = array([self.game_dimensions[0],
                        self.game_dimensions[1],
                        0])

        p10, p11, p12, p20, p21, p22, p30, p31, p32 = trace_rob_game(q)

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

    def simulate(self):
        """simulate on pygame the robot and its displacements
        """
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
            old_q = self.q
            self.q = mgi_analytique(self.pos_eff)
            if isinstance(self.q, int):
                self.q = old_q
            if keys[pygame.K_s]:
                self.pos_eff[1] += 0.001
                self.pos_eff[1] = min(1, self.pos_eff[1])
            elif keys[pygame.K_z]:
                self.pos_eff[1] -= 0.001
                self.pos_eff[1] = max(-1, self.pos_eff[1])
            elif keys[pygame.K_q]:
                self.pos_eff[0] -= 0.001
                self.pos_eff[0] = max(-1, self.pos_eff[0])
            elif keys[pygame.K_d]:
                self.pos_eff[0] += 0.001
                self.pos_eff[0] = min(1, self.pos_eff[0])
            elif keys[pygame.K_e]:
                self.pos_eff[2] += 0.01
                self.pos_eff[2] = min(1, self.pos_eff[2])
            elif keys[pygame.K_a]:
                self.pos_eff[2] -= 0.01
                self.pos_eff[2] = max(-1, self.pos_eff[2])
            self.pos.append(self.pos_eff)
            self.clock.append(self.clock[-1] + self.step)
            self.draw(screen)

            # time_text = font.render(f"Time: {round(self.clock[-1], 1)}", True, (0, 0, 0))
            # text_rect = time_text.get_rect(bottomright=(self.game_dimensions[0] - 10, self.game_dimensions[1] - 10))
            # screen.blit(time_text, text_rect)

            pygame.display.flip()

            if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
                self.running = False
                pygame.quit()
                return ("fin")


if __name__ == '__main__':
    robot = Robot3RRR()
    robot.game = True
    robot.q = mgi_analytique(robot.pos_eff)
    # robot.draw()
    robot.simulate()
