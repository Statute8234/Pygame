import pygame
import random, sys, time
import math
import Items
pygame.init()
current_time = time.time()
random.seed(current_time)

# screen
WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space')
clock = pygame.time.Clock()

# colors
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "DIM_GRAY": (105, 105, 105)
}

all_sprites = pygame.sprite.Group()

# Asteroid
asteroid_group = pygame.sprite.Group()
asteroid_list = [r'assets\asteroid.png',r'assets\asteroid_green.png']
for x in range(random.randint(1,50)):
    while True:
        size = random.uniform(10,30)
        position = [random.uniform(size,WIDTH - size), random.uniform(size,HEIGHT - size)]
        asteroid = Items.Asteroid(position[0],position[1], size, size, random.choice(asteroid_list))
        if not pygame.sprite.spritecollideany(asteroid, asteroid_group):
            asteroid_group.add(asteroid)
            break
all_sprites.add(asteroid_group)

# player
playerShips_list = pygame.sprite.Group()
spacing = 40
for x in range(3):
    player = Items.Player((WIDTH / 2) + x * 40, HEIGHT - 20, 30, 30, r'assets\spaceship.png',r'assets\close.png')
    player.active = True
    playerShips_list.add(player)
all_sprites.add(playerShips_list)

player_pos = pygame.Vector2(player.rect.centerx, player.rect.centery)
player_velocity = pygame.Vector2(0, 0)
start_pos = None
start_time = None
is_dragging = False

# lines
lines_list = pygame.sprite.Group()
player_line = Items.Line((0,HEIGHT - 50),(WIDTH,HEIGHT - 50),colors['BLUE'], 2, WIDTH, HEIGHT)
CPU_line = Items.Line((0,50),(WIDTH,50),colors['RED'], 2, WIDTH, HEIGHT)
lines_list.add(player_line)
lines_list.add(CPU_line)
all_sprites.add(lines_list)

def main():
    global player_pos, player_velocity, start_pos, start_time, is_dragging
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not is_dragging:
                    is_dragging = True
                    start_pos = pygame.Vector2(pygame.mouse.get_pos())
                    start_time = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONUP:
                if is_dragging:
                    is_dragging = False
                    end_pos = pygame.Vector2(pygame.mouse.get_pos())
                    end_time = pygame.time.get_ticks()
                    duration = (end_time - start_time) / 1000
                    distance = (end_pos - start_pos).length()
                    if distance != 0:
                        direction = (end_pos - start_pos).normalize()
                    else:
                        direction = pygame.Vector2(0, 0)
                    speed = min(distance / duration, 100)
                    player_velocity = direction * speed

        screen.fill(colors['DIM_GRAY'])

        if is_dragging:
            current_pos = pygame.Vector2(pygame.mouse.get_pos())
            pygame.draw.line(screen, colors['RED'], start_pos, current_pos, 2)
        
        player_pos += -(player_velocity * clock.get_time() / 1000)
        player_velocity *= 0.99
        
        all_sprites.update()
        all_sprites.draw(screen)
        
        for player in playerShips_list:
            if not player.active:
                player.deactivePlayer(screen)

        active_player = None
        for idx, player in enumerate(playerShips_list):
            if player.active:
                active_player = player
                current_player_index = idx
                break
        
        if active_player:
            active_player.rotate(mouse_pos)
            active_player.move(player_pos)
        
        # check for collisions
        if pygame.sprite.spritecollideany(active_player, asteroid_group):
            active_player.active = False
            player_velocity = pygame.Vector2(0, 0)
            # move player
            next_player_index = (current_player_index + 1) % len(playerShips_list)
            next_player = list(playerShips_list)[next_player_index]
            next_player.active = True
            player_pos = pygame.Vector2(next_player.rect.center)

        """Check collision with lines"""
        if pygame.sprite.spritecollideany(active_player, lines_list):
            active_player.active = False
            player_velocity = pygame.Vector2(0, 0)
            
        clock.tick(64)
        pygame.display.flip()

if __name__ == "__main__":
    main()