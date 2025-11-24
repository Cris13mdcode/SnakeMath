import pygame
import sys


def main():
    # --- Inițializare pygame ---
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test publicare - imagine rotită")
    clock = pygame.time.Clock()

    # --- Creăm o "imagine" simplă (un pătrat colorat) ---
    # Nu depindem de fișiere externe, ca să fie proiectul cât mai simplu.
    size = 150
    base_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    base_surf.fill((0, 180, 255))          # albastru deschis
    pygame.draw.rect(base_surf, (255, 255, 255), (10, 10, size - 20, size - 20), 8)

    angle = 0

    # Text ajutor
    font = pygame.font.Font(None, 32)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Patru taste care setează unghiul imaginii
                if event.key == pygame.K_UP:
                    angle = 0          # sus
                if event.key == pygame.K_RIGHT:
                    angle = -90        # dreapta
                if event.key == pygame.K_DOWN:
                    angle = 180        # jos
                if event.key == pygame.K_LEFT:
                    angle = 90         # stânga

        screen.fill((30, 30, 30))

        # Rotim imaginea și o desenăm în centru
        rotated = pygame.transform.rotate(base_surf, angle)
        rect = rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(rotated, rect)

        # Instrucțiuni pe ecran
        text = font.render("Foloseste sagetile (↑ ↓ ← →) pentru rotire, ESC pentru iesire", True, (220, 220, 220))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()



