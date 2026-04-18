
import pygame
import sys

# --- Configuration & Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (8-bit Palette)
DAY_SKY = (135, 206, 235)
NIGHT_SKY = (20, 24, 82)
GRASS_GREEN = (34, 139, 34)
DIRT_BROWN = (101, 67, 33)
PIG_PINK = (255, 182, 193)
WOLF_GRAY = (50, 50, 50)
BUSH_DARK_GREEN = (0, 100, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40)) # Square Pig
        self.image.fill(PIG_PINK)
        self.rect = self.image.get_rect(midbottom=(100, 500))
        self.vel_y = 0
        self.speed = 5
        self.is_jumping = False
        self.hiding = False

    def apply_gravity(self):
        self.vel_y += 0.8
        self.rect.y += self.vel_y
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.is_jumping = False

    def update(self, keys, bushes):
        # Movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Jump
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.vel_y = -16
            self.is_jumping = True

        # Stealth Check
        self.hiding = False
        for bush in bushes:
            if self.rect.colliderect(bush.rect):
                self.hiding = True

class Wolf(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(WOLF_GRAY)
        self.rect = self.image.get_rect(topleft=(800, 460))
        self.active = False

    def update(self, player):
        if self.active and not player.hiding:
            if self.rect.x < player.rect.x:
                self.rect.x += 3
            else:
                self.rect.x -= 3

class StaticObject(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Game Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Veluwe Venture: Spek-takel")
clock = pygame.time.Clock()

player = Player()
wolf = Wolf()
bushes = [StaticObject(300, 460, 60, 40, BUSH_DARK_GREEN), 
          StaticObject(600, 460, 60, 40, BUSH_DARK_GREEN)]
all_sprites = pygame.sprite.Group(player, wolf)

game_time = 0 # Track day/night cycle

# --- Main Game Loop ---
while True:
    game_time += 1
    is_night = (game_time // 300) % 2 == 1 # Swap every 5 seconds for demo
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    # Logic
    player.update(keys, bushes)
    wolf.active = is_night
    wolf.update(player)

    # Collision: Wolf catches Pig
    if wolf.active and player.rect.colliderect(wolf.rect) and not player.hiding:
        print("THE WOLF GOT YOU!")
        game_time = 0 # Reset
        player.rect.midbottom = (100, 500)

    # Rendering
    bg_color = NIGHT_SKY if is_night else DAY_SKY
    screen.fill(bg_color)
    
    # Draw Ground
    pygame.draw.rect(screen, GRASS_GREEN, (0, 500, SCREEN_WIDTH, 100))
    
    # Draw Bushes
    for bush in bushes:
        screen.blit(bush.image, bush.rect)
    
    # Draw Sprites
    all_sprites.draw(screen)
    
    # UI Text
    font = pygame.font.Font(None, 36)
    mode_text = "NIGHT - RUN/HIDE!" if is_night else "DAY - CHILL"
    text_surf = font.render(mode_text, True, (255, 255, 255))
    screen.blit(text_surf, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)