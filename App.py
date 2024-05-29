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
turns = 1

# colors
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "DIM_GRAY": (105, 105, 105),
    "GRAY": (128,128,128)
}

all_sprites = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
playerShips_list = pygame.sprite.Group()
CPUShips_list = pygame.sprite.Group()
lines_list = pygame.sprite.Group()

# Asteroid
asteroid_list = [r'assets\asteroid.png',r'assets\asteroid_green.png']
def populate_asteroid():
    for asteroid in range(random.randint(1,50)):
        while True:
            size = random.uniform(10,30)
            position = [random.uniform(size,WIDTH - size), random.uniform(size,HEIGHT - size)]
            asteroid = Items.Asteroid(position[0],position[1], size, size, random.choice(asteroid_list))
            if not pygame.sprite.spritecollideany(asteroid, asteroid_group):
                asteroid_group.add(asteroid)
                break
    all_sprites.add(asteroid_group)

# player
player_pos = None
player_velocity = None
start_pos = None
start_time = None
is_dragging = False
current_player_index = 0
# CPU 
active_CPU = None
player_line_y = HEIGHT - 50
target_pos = (random.uniform(0, WIDTH), player_line_y)
current_CPU_index = 0

def populate_players():
    global player_pos, player_velocity
    spacing = 40
    for x in range(3):
        player = Items.Player((WIDTH / 2) + x * 40, HEIGHT - 20, 30, 30, r'assets\spaceship.png',r'assets\close.png')
        if (x == 0):
            player.active = True
            player_pos = pygame.Vector2(player.rect.centerx, player.rect.centery)
            player_velocity = pygame.Vector2(0, 0)
        playerShips_list.add(player)
    
    for x in range(3):
        CPU_player = Items.Player((WIDTH / 2) + x * 40, 20, 30, 30, r'assets\space-ship.png',r'assets\close.png')
        if (x == 0):
            CPU_player.active = True
        CPUShips_list.add(CPU_player)

    all_sprites.add(CPUShips_list, playerShips_list)

# lines
def populate_lines():
    player_line = Items.Line((0,HEIGHT - 50),(WIDTH,HEIGHT - 50),colors['BLUE'], 2, WIDTH, HEIGHT)
    CPU_line = Items.Line((0,50),(WIDTH,50),colors['RED'], 2, WIDTH, HEIGHT)
    lines_list.add(player_line)
    lines_list.add(CPU_line)
    all_sprites.add(lines_list)

# restart Game()
def restart_game_func():
    global asteroid_group, playerShips_list, lines_list, player_pos, player_velocity, current_player_index
    asteroid_group.empty()
    playerShips_list.empty()
    CPUShips_list.empty()
    lines_list.empty()
    all_sprites.empty()

    populate_asteroid()
    populate_players()
    populate_lines()

    current_player_index = 0

def findNextPlayer():
    global current_player_index, player_pos, player_velocity
    # Deactivate the current player
    if playerShips_list:
        current_player = list(playerShips_list)[current_player_index]
        current_player.active = False

    # Move to the next player
    current_player_index = (current_player_index + 1) % len(playerShips_list)
    next_player = list(playerShips_list)[current_player_index]
    next_player.active = True

    # Update the player's position and velocity
    player_pos = pygame.Vector2(next_player.rect.center)
    player_velocity = pygame.Vector2(0, 0)


def findNextCPU():
    global current_CPU_index, target_pos
    current_CPU_index = (current_CPU_index + 1) % len(CPUShips_list)
    next_CPU = list(CPUShips_list)[current_CPU_index]
    if next_CPU.active == False:
        target_pos = (random.uniform(0, WIDTH), player_line_y)
    next_CPU.active = True

# button
playButton = Items.button((WIDTH / 2) - 50, (HEIGHT / 2) - 50, 100, 100, "Play", colors['GREEN'], colors['GRAY'])

def main():
    global player_pos, player_velocity, start_pos, start_time, is_dragging, current_player_index, current_CPU_index, target_pos, turns, active_CPU
    play_game = False
    active_player = None
    # loop
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
                    speed = min(distance // duration, 100)
                    player_velocity = direction * speed
                    turns += 1

            if not play_game:
                playButton.handle_event(event)
                if playButton.clicked:
                    play_game = True
                    playButton.reset()
                    restart_game_func()

        screen.fill(colors['DIM_GRAY'])

        if not play_game:
            playButton.draw(screen)
        else:
            all_sprites.update()
            all_sprites.draw(screen)

            # show removed player
            for player in all_sprites:
                try:
                    if player.dead:
                        player.deactivePlayer(screen)
                except:
                    pass
            
            """Players turn"""
            if (turns % 2) == 0:
                player_pos += -(player_velocity * clock.get_time() / 1000)
                player_velocity *= 0.99

                for idx, player in enumerate(playerShips_list):
                    if player.active and not player.dead:
                        active_player = player
                        current_player_index = idx
                        break

                if active_player:
                    active_player.rotate(mouse_pos)
                    active_player.move(player_pos)
                    if player_pos.y <= 50:
                        findNextPlayer()

            else:  # CPU's turn
                for idx_CPU, CPU_player in enumerate(CPUShips_list):
                    if CPU_player.active and not CPU_player.dead:
                        active_CPU = CPU_player
                        current_CPU_index = idx_CPU
                        break

                if active_CPU:
                    active_CPU.move_towards(target_pos)
                    if active_CPU.move_towards(target_pos) <= 0:
                        active_CPU.distance = random.randint(0,100)
                        turns += 1
            # check for dragging
            if is_dragging:
                current_pos = pygame.Vector2(mouse_pos)
                pygame.draw.line(screen, colors['RED'], start_pos, current_pos, 2)

            # check for collisions
            try:
                if active_player and pygame.sprite.spritecollideany(active_player, asteroid_group):
                    active_player.dead = True
                    active_player.active = False
                    findNextPlayer()

                if active_CPU and pygame.sprite.spritecollideany(active_CPU, asteroid_group):
                    active_CPU.dead = True
                    active_CPU.active = False
                    findNextCPU()
                
                for CPU_player in CPUShips_list:
                    if CPU_player.rect.centery >= player_line_y:
                        active_CPU.speed = 0
                        active_CPU.dead = False
                        active_CPU.active = True
                        findNextCPU()
                
                """-- end game --"""
                if all(player.y >= HEIGHT - 50 for player in playerShips_list):
                    if all(player.dead or not player.active for player in playerShips_list):
                        play_game = False

            except Exception as e:
                print(f"Error: {e}")
                play_game = False
        
        clock.tick(64)
        pygame.display.flip()

if __name__ == "__main__":
    main()
