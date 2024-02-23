import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
TANK_SPEED = 5
BULLET_SPEED = 10
NUM_TARGETS = 5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game")

# Load and resize tank image, bullet image, and target image
tank_img = pygame.image.load("tank.png")
tank_img = pygame.transform.scale(tank_img, (50, 50))  # Resize tank image
bullet_img = pygame.image.load("bullet.jpg")
bullet_img = pygame.transform.scale(bullet_img, (20, 20))  # Resize bullet image
target_img = pygame.image.load("target3.jpg")
target_img = pygame.transform.scale(target_img, (50, 50))  # Resize target image
win_img = pygame.image.load("win.png")
win_img = pygame.transform.scale(win_img, (WIDTH, HEIGHT))  # Resize win image

# Tank properties
tank_rect = tank_img.get_rect()
tank_rect.topleft = (0, HEIGHT - 200)  # Start in the middle of the screen vertically
tank_angle = 0

# Text input
font = pygame.font.Font(None, 36)
message = " "
current_message = ""
message_index = 0

# Bullet properties
bullets = []
bullet_angles = []  # Store the angles for each bullet
# Target properties
targets = [target_img.get_rect(topleft=(x, y)) for x, y in [(100, 100), (200, 300), (400, 200), (600, 400), (700, 100)]]
targets_hit = [False] * NUM_TARGETS

# Target properties
target_rect = target_img.get_rect()
target_rect.topleft = (
WIDTH - target_rect.width, HEIGHT // 2 - target_rect.height // 2)  # Start in the middle of the screen vertically

# Win properties
win_count = 0


def draw_text(message, x, y):
    text = font.render(message, True, WHITE)
    screen.blit(text, (x, y))


# Main game loop
clock = pygame.time.Clock()

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tank_angle += 5
    if keys[pygame.K_RIGHT]:
        tank_angle -= 5
    if keys[pygame.K_UP]:
        tank_rect.y -= TANK_SPEED
    if keys[pygame.K_DOWN]:
        tank_rect.y += TANK_SPEED

    if keys[pygame.K_SPACE]:
        # Shoot a bullet
        bullet = {
            "rect": bullet_img.get_rect(center=(tank_rect.centerx, tank_rect.centery)),
            "angle": tank_angle,
            "lifetime": 5 * FPS  # Adjust lifetime (5 seconds)
        }
        bullets.append(bullet)
        current_message += message[message_index]
        message_index = (message_index + 1) % len(message)

    bullets = [bullet for bullet in bullets if bullet["lifetime"] > 0]  # Remove bullets with zero lifetime

    for bullet in bullets:
        # Move the bullet
        bullet["rect"].move_ip(BULLET_SPEED * pygame.math.Vector2(1, 0).rotate(-bullet["angle"]))

        # Check collision with the targets
        for i, target in enumerate(targets):
            if target.colliderect(bullet["rect"]) and not targets_hit[i]:
                targets_hit[i] = True
                bullet["lifetime"] = 0  # Stop the bullet upon hitting a target
                current_message = f"Hit target {i + 1}!"

        # Draw the bullet
        screen.blit(pygame.transform.rotate(bullet_img, bullet["angle"]), bullet["rect"])

    rotated_tank = pygame.transform.rotate(tank_img, tank_angle)
    tank_rect = rotated_tank.get_rect(topleft=(tank_rect.x, tank_rect.y))
    screen.blit(rotated_tank, tank_rect)

    for i, target in enumerate(targets):
        if not targets_hit[i]:
            screen.blit(target_img, target)

    draw_text(current_message, 10, HEIGHT - 40)
    draw_text("Press SPACE to shoot", 10, HEIGHT - 80)

    # Check if all targets are hit to display the win image
    if all(targets_hit):
        screen.blit(win_img, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)
