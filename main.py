import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hawking Dodge")

BG = pygame.transform.scale(pygame.image.load("black hole.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 10
PLAYER_HEIGHT = 20

PLAYER_VEL = 10
PARTICLE_WIDTH = 10
PARTICLE_HEIGHT = 20
PARTICLE_VEL = 5

FONT = pygame.font.SysFont("calibri", 30)


def draw(player, elapsed_time, particles):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "yellow", player)

    for particle in particles:
        pygame.draw.rect(WIN, "orange", particle)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    particle_add_increment = 2000
    particle_count = 0

    particles = []
    hit = False

    while run:
        particle_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if particle_count > particle_add_increment:
            for _ in range(5):
                particle_x = random.randint(0, WIDTH - PARTICLE_WIDTH)
                particle = pygame.Rect(particle_x, -PARTICLE_HEIGHT,
                                   PARTICLE_WIDTH, PARTICLE_HEIGHT)
                particles.append(particle)

            particle_add_increment = max(50, particle_add_increment - 50)
            particle_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_SEMICOLON]: particle_count += clock.tick(10)

        for particle in particles[:]:
            particle.y += PARTICLE_VEL
            if particle.y > HEIGHT:
                particles.remove(particle)
            elif particle.y + particle.height >= player.y and particle.colliderect(player):
                particles.remove(particle)
                hit = True
                break

        if hit:
            lost_text = FONT.render("ANNIHILATED", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, particles)

    pygame.quit()


if __name__ == "__main__":
    main()