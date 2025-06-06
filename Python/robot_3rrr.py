"""test for a 3rrr class"""

import numpy as np
from numpy import pi, array, cos, sin, atan2, sqrt, acos
import matplotlib.pyplot as plt
import pygame
from singularity import *
import pygame.locals
import math

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
                if not self.interpolate:
                    print("[ERREUR] -- problème d'atteignabilité")
                return 0
            alpha = atan2(y, x) - atan2(self.l2*sin(beta), self.l1+self.l2*cos(beta))
            q = np.append(q, alpha)
            q = np.append(q, beta)
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
        plt.plot([p10[0], p11[0], p12[0]], [-p10[1], -p11[1], -p12[1]])
        plt.plot([p20[0], p21[0], p22[0]], [-p20[1], -p21[1], -p22[1]])
        plt.plot([p30[0], p31[0], p32[0]], [-p30[1], -p31[1], -p32[1]])
        plt.plot([p12[0], p22[0], p32[0], p12[0]],
                [-p12[1], -p22[1], -p32[1], -p12[1]], linewidth=2)
        x_array = []
        y_array = []
        for i in range(len(self.pos)):
            x_array.append(self.pos[i][0])
            y_array.append(- self.pos[i][1])
        plt.plot(x_array, y_array,'.b')
        plt.axis("square")
        plt.axis("equal")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Dernière position du robot et trajectoire")
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

        if abs(detA) < 0.01:
            if gamma1/pi == gamma2/pi and gamma2/pi == gamma3/pi:
                print("Singularité parallèle, les trois droites sont parallèles.")
            else:
                print("Singularité parallèle, les trois droites sont concourantes.")
        if detB == 0:
            print("Singularité série, le bras 3 est à la limite de son espace de travail.")

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

        # Affichage des commandes
        if not self.interpolate:
            font = pygame.font.SysFont("Arial", 16)
            commands = [
                "Commandes:",
                "'A' : Rotation sens trigonométrique",
                "'E' : Rotation sens horaire",
                "ZQSD : Déplacement",
                "'T' - Crayon ON/OFF",
                "'Esc' ou 'SPACE' - Quitter",
            ]

            for i, line in enumerate(commands):
                text_surface = font.render(line, True, (0, 0, 0))
                screen.blit(text_surface, (10, 10 + i * 20))  # position verticale espacée

    def segment_distance(self, p1, p2, q1, q2):
        """Retourne la distance minimale entre deux segments en 2D"""
        def dot(a, b):
            return np.dot(a, b)

        def norm(a):
            return np.linalg.norm(a)

        def clamp(x, a, b):
            return max(a, min(x, b))

        p1, p2, q1, q2 = np.array(p1), np.array(p2), np.array(q1), np.array(q2)
        d1 = p2 - p1
        d2 = q2 - q1
        r = p1 - q1
        a = dot(d1, d1)
        e = dot(d2, d2)
        f = dot(d2, r)

        if a <= 1e-8 and e <= 1e-8:
            return norm(p1 - q1)
        if a <= 1e-8:
            s = 0
            t = clamp(f / e, 0, 1)
        else:
            c = dot(d1, r)
            if e <= 1e-8:
                t = 0
                s = clamp(-c / a, 0, 1)
            else:
                b = dot(d1, d2)
                denom = a * e - b * b
                if denom != 0:
                    s = clamp((b * f - c * e) / denom, 0, 1)
                else:
                    s = 0
                t = (b * s + f) / e
                if t < 0:
                    t = 0
                    s = clamp(-c / a, 0, 1)
                elif t > 1:
                    t = 1
                    s = clamp((b - c) / a, 0, 1)

        closest_point_p = p1 + d1 * s
        closest_point_q = q1 + d2 * t
        return norm(closest_point_p - closest_point_q)

    def check_collision(self, q):
        p10, p11, p12, p20, p21, p22, p30, p31, p32 = self.trace_rob_game(q)

        seuil_epaisseur = 0.05  # Ajuste en fonction de la taille de tes bras

        if self.segment_distance(p11[:2], p12[:2], p21[:2], p22[:2]) < seuil_epaisseur:
            return True
        if self.segment_distance(p11[:2], p12[:2], p31[:2], p32[:2]) < seuil_epaisseur:
            return True
        if self.segment_distance(p21[:2], p22[:2], p31[:2], p32[:2]) < seuil_epaisseur:
            return True
        return False

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

    def interpolate_path(self, points, n_steps=50, fps=30):
        self.interpolate = True
        self.fps = fps

        if not self.game:
            return

        pygame.init()
        screen = pygame.display.set_mode(self.game_dimensions)
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return "fin"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        running = False
                        pygame.quit()
                        return "fin"

            for i in range(len(points) - 1):
                p_start = np.array(points[i])
                p_end = np.array(points[i + 1])

                # Optimiser l'orientation pour le point de départ et le point d'arrivée
                start_orientation = self.optimize_orientation(p_start)
                end_orientation = self.optimize_orientation(p_end)

                for t in np.linspace(0, 1, n_steps):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            return "fin"
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                                running = False
                                pygame.quit()
                                return "fin"

                    p_interp = (1 - t) * p_start + t * p_end
                    # Interpoler l'orientation
                    p_interp[2] = (1 - t) * start_orientation + t * end_orientation

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

    def optimize_orientation(self, pos_eff):
        orientation_center = pos_eff[2]
        q_ref = self.q if hasattr(self, 'q') else None

        best_orientation = orientation_center
        min_joint_jump = float('inf')
        detA_threshold = 0.01  # à ajuster

        candidate_orientations = np.linspace(orientation_center - np.pi, orientation_center + np.pi, 30)

        for candidate_orientation in candidate_orientations:
            pos_eff[2] = candidate_orientation
            q = self.mgi_analytique(pos_eff)

            if isinstance(q, int):  # Inatteignable
                continue

            if self.check_collision(q): # Collision
                continue

            # Calcul du déterminant Jacobien approx (via trace_rob_game)
            p10, p11, p12, p20, p21, p22, p30, p31, p32 = self.trace_rob_game(q)
            
            gamma1 = atan2(p12[1]-p11[1], p12[0] - p11[0])
            gamma2 = atan2(p22[1]-p21[1], p22[0] - p21[0])
            gamma3 = atan2(p32[1]-p31[1], p32[0] - p31[0])

            d1 = (self.pos_eff-p12).dot(array([-sin(gamma1),cos(gamma1),1]))
            d2 = (self.pos_eff-p22).dot(array([-sin(gamma2),cos(gamma2),1]))
            d3 = (self.pos_eff-p32).dot(array([-sin(gamma3),cos(gamma3),1]))


            detA = abs(det_A(gamma1, gamma2, gamma3, d1, d2, d3))
            if detA < detA_threshold:
                continue  # Trop proche singularité

            # Priorité à la continuité des articulations
            if q_ref is not None:
                joint_jump = np.linalg.norm(np.array(q) - np.array(q_ref))
            else:
                joint_jump = 0  # Premier point

            if joint_jump < min_joint_jump:
                min_joint_jump = joint_jump
                best_orientation = candidate_orientation

        pos_eff[2] = best_orientation  # restore
        return best_orientation

    def trace_square(self, height=0.07, n_steps=100, fps=60):
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

        self.interpolate_path(square_points, n_steps=n_steps, fps=fps)

    def trace_circle(self, center=(0.0, 0.0), radius=0.07, N=100, n_steps=10, fps=60):
        """Trace un cercle"""

        circle_points = []
        angles = np.linspace(0, 2 * pi, N)

        for angle in angles:
            # Calcul de la position cible sur le cercle
            x = center[0] + radius * cos(angle)
            y = center[1] + radius * sin(angle)
            circle_points.append([x, y, 0])

        self.interpolate_path(circle_points, n_steps=n_steps, fps=fps)

    def trace_trefle(self, gain=0.02, N=100, n_steps=10, fps=60):
        """Trace un trèfle"""
        trefle_points = []

        trefle = np.linspace(0, 2 * pi, N)

        for t in trefle:
            r = gain * (1 + np.cos(4 * t) + 2 * (np.sin(4 * t))**2)
            x = r * np.cos(t)
            y = r * np.sin(t)
            trefle_points.append([x, y, 0])

        self.interpolate_path(trefle_points, n_steps=n_steps, fps=fps)

    def trace_polygone(self, points_list, n_steps=100, fps=30):
        """Trace un polygone"""

        self.pos = []
        self.pen = True

        self.interpolate_path(points_list, n_steps=n_steps, fps=fps)
if __name__ == '__main__':

    test_control = 1
    test_square = 0
    test_circle = 0
    test_trefle = 0
    test_polygone = 0

    robot = Robot3RRR()
    robot.game = True

    if test_control:
        robot.q = robot.mgi_analytique(robot.pos_eff)
        robot.simulate()
        robot.game = False
        robot.draw()

    # Les orientations des formes ci-dessous seront optimisées pour s'éloigner du mieux possible des singularités
    # Le but étant de s'éloigner le plus possible des lignes concourantes

    if test_square:
        robot.trace_square()    # Rester appuyé sur échap pour quitter

    if test_circle:
        robot.trace_circle()    # Rester appuyé sur échap pour quitter

    if test_trefle:
        robot.trace_trefle()    # Rester appuyé sur échap pour quitter

    if test_polygone:
        points_list = [[0, 0, 0], [-0.03, 0.08, 0], [0.08, -0.02, 0], [-0.01, -0.04, 0], [-0.06, 0.04, 0], [0,0,0]]
        robot.trace_polygone(points_list=points_list)    # Rester appuyé sur échap pour quitter
