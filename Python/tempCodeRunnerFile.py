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