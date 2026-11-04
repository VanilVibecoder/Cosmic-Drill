import pygame
import random

# Initialize pygame
pygame.init()

# Create clock for dt
clock = pygame.time.Clock()

# Initialize fonts
font = pygame.font.SysFont("Arial", 24)

# Create screen, title and icon
WINDOW = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Cosmic Drill")
icon = pygame.image.load("spaceship(1).png")
pygame.display.set_icon(icon)

# Background
background_img = pygame.image.load("space_background.jpg")
background_img = pygame.transform.scale(background_img, (600, 800))

# Spaceship load
spaceship_img = pygame.image.load("shuttle2.png").convert_alpha()
spaceship_img = pygame.transform.scale(spaceship_img, (50, 55))

# Enemy load
enemy_img = pygame.image.load("alien.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

# Bullet load
bullet_img = pygame.image.load("bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (15, 15))

# Heart load
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (30, 30))

# Position the spaceship in the center of the screen
space_rect = spaceship_img.get_rect()
space_rect.centerx = 300
space_rect.bottom = 780
player_x_float = float(space_rect.x)

# Bullet settings
bullet_speed = 300
bullets = []

# Player settings
player_speed = 310
player_hp = 3
player_hitbox = pygame.Rect(0, 0, 10, 10)
player_hitbox.center = space_rect.center

# Draw spaceship on the screen
def player(x, y):
    WINDOW.blit(spaceship_img, (x, y))

# Draw enemy on the screen
def enemy(x, y):
    WINDOW.blit(enemy_img, (x, y))

# Check collision between a bullet and an enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    enemy_rect = pygame.Rect(int(enemyX), int(enemyY), 50, 50)
    bullet_rect = pygame.Rect(int(bulletX), int(bulletY), 15, 15)
    return enemy_rect.colliderect(bullet_rect)

# Start state of game
game_state = "MENU"
running = True

# Difference between frames in seconds
dt = 0

# World speed down the screen
world_speed = 120

# List of enemies on the screen
enimies = []

# Timer for spawning enemies
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1500)

# Score
score_value = 0
scoreX = 10
scoreY = 10

def draw_score(x, y):
    text = font.render(f"Score: {score_value}", True, (255, 255, 255))
    WINDOW.blit(text, (x, y))

# Game loop
while running:
    # Clear the screen and draw background
    WINDOW.fill((10, 10, 26))
    WINDOW.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "MENU" and event.key == pygame.K_SPACE:
                game_state = "PLAY"

            elif game_state == "PLAY" and event.key == pygame.K_SPACE:
                # Fire a bullet from the center of the ship
                start_x = space_rect.centerx - bullet_img.get_width() / 2
                start_y = space_rect.top
                bullets.append({"X": start_x, "Y": start_y})

            elif game_state == "GAME_OVER" and event.key == pygame.K_r:
                # Reset game data and restart
                player_hp = 3
                score_value = 0
                bullets.clear()
                enimies.clear()
                space_rect.centerx = 300
                player_x_float = float(space_rect.x)
                player_hitbox.center = space_rect.center
                game_state = "PLAY"

        if event.type == SPAWN_ENEMY and game_state == "PLAY":
            new_enemy_on_x = random.randint(0, 600 - 50)
            new_enemy_on_y = random.randint(-100, -40)
            enimies.append({"X": new_enemy_on_x, "Y": new_enemy_on_y})

    if game_state == "MENU":
        surf = font.render("Press Space to start", True, (220, 220, 220))
        text_rect = surf.get_rect()
        text_rect.center = (300, 400)
        WINDOW.blit(surf, text_rect)

    if game_state == "PLAY":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            player_x_float += player_speed * dt

        if keys[pygame.K_a]:
            player_x_float -= player_speed * dt

        # Update ship position before checking collisions
        space_rect.x = int(player_x_float)

        if space_rect.right > 600:
            space_rect.right = 600
            player_x_float = float(space_rect.x)

        if space_rect.left < 0:
            space_rect.left = 0
            player_x_float = float(space_rect.x)

        # Keep the player's hitbox at the center of the ship
        player_hitbox.center = space_rect.center

        # Move bullets upward
        for b in bullets:
            b["Y"] -= bullet_speed * dt

        # Move enemies downward
        for e in enimies:
            e["Y"] += world_speed * dt

        # Check bullet collisions with enemies
        for b in bullets:
            for e in enimies:
                if e["Y"] == 9999:
                    continue  # Already destroyed this frame
                if isCollision(e["X"], e["Y"], b["X"], b["Y"]):
                    b["Y"] = -999
                    e["Y"] = 9999
                    score_value += 10
                    break

        # Check enemy collisions with player's small hitbox
        for e in enimies:
            if e["Y"] == 9999:
                continue  # Skip enemies destroyed by bullets
            enemy_rect = pygame.Rect(int(e["X"]), int(e["Y"]), 50, 50)
            if player_hitbox.colliderect(enemy_rect):
                e["Y"] = 9999
                player_hp = max(0, player_hp - 1)

        # Delete destroyed or off-screen objects
        bullets = [b for b in bullets if b["Y"] + 15 > 0 and b["Y"] != -999]
        enimies = [e for e in enimies if e["Y"] < 800 and e["Y"] != 9999]

        draw_score(scoreX, scoreY)

        # Draw remaining HP
        for i in range(player_hp):
            heart_x = 460 + (i * 40)
            heart_y = 20
            WINDOW.blit(heart_img, (heart_x, heart_y))

        # End the game when all HP are lost
        if player_hp == 0:
            game_state = "GAME_OVER"

    # Draw spaceship, enemies and bullets
    player(space_rect.x, space_rect.y)
    for e in enimies:
        enemy(e["X"], e["Y"])
    for b in bullets:
        WINDOW.blit(bullet_img, (int(b["X"]), int(b["Y"])))

    if game_state == "GAME_OVER":
        # Show final score and restart prompt
        game_over_text = font.render("GAME OVER", True, (255, 80, 80))
        final_score_text = font.render(f"Score: {score_value}", True, (255, 255, 255))
        restart_text = font.render("Press R to restart", True, (255, 255, 255))

        WINDOW.blit(game_over_text, game_over_text.get_rect(center=(300, 350)))
        WINDOW.blit(final_score_text, final_score_text.get_rect(center=(300, 400)))
        WINDOW.blit(restart_text, restart_text.get_rect(center=(300, 450)))

    # Update the display and calculate dt in seconds
    pygame.display.flip()
    dt = clock.tick(60) / 1000.0

pygame.quit()
