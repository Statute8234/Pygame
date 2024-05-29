import pygame
import random, sys, time
import math

colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "DIM_GRAY": (105, 105, 105),
    "GRAY": (128,128,128)
}

# Asteroid
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, imagePath):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = pygame.image.load(imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0

# player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, imagePath, deactiveImage):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.deactiveImage = deactiveImage
        self.original_image = pygame.image.load(imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0
        self.active = False
        self.dead = False
        self.speed = 2
        self.distance = random.randint(0,100)

    def rotate(self, mouse_pos):
        if self.active:
            rel_mouse_x, rel_mouse_y = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
            self.angle = (180 / math.pi) * -math.atan2(rel_mouse_y, rel_mouse_x)
            self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (self.width, self.height)), self.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)
    
    def distance_t0_position(self, new_position):
        currentPosition = pygame.Vector2(self.rect.center)
        new_positionVector = pygame.Vector2(new_position)
        return currentPosition.distance_to(new_positionVector)
    
    def move(self, newPosition):
        if self.active:
            self.rect.center = newPosition

    def deactivePlayer(self, screen):
        self.dead = True
        self.deactiveOriginal_image = pygame.image.load(self.deactiveImage).convert_alpha()
        self.deactive_image = pygame.transform.scale(self.deactiveOriginal_image, (self.width, self.height))
        screen.blit(self.deactive_image, (self.rect.centerx - self.width / 2,self.rect.centery - self.height / 2))

    def move_towards(self, target_pos):
        if self.active and not self.dead:
            if self.distance > 0:
                if (self.rect.centerx != target_pos[0]):
                    if self.rect.centerx > target_pos[0]:
                        self.rect.centerx -= self.speed
                    if self.rect.centerx < target_pos[0]:
                        self.rect.centerx += self.speed
                if (self.rect.centery != target_pos[1]):
                    if self.rect.centery > target_pos[1]:
                        self.rect.centery -= self.speed
                    if self.rect.centery < target_pos[1]:
                        self.rect.centery += self.speed
                self.distance -= self.speed
        return self.distance
# lines
class Line(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, color, width, WIDTH, HEIGHT):
        super().__init__()
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.width = width
        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.draw()

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.line(self.image, self.color, self.start_pos, self.end_pos, self.width)  # Draw the line

# button 
class button:
    def __init__(self, x, y, width, height, text, active_color, inactive_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.textColor = colors["BLACK"]
        self.origional_textColor = self.textColor
        self.fontSize = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.fontSize)
        self.clicked = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.color = self.active_color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
                    self.textColor = self.active_color
                    self.color = self.active_color
        else:
            self.color = self.inactive_color
            self.textColor = self.origional_textColor
    
    def reset(self):
        self.clicked= False
        self.color = self.inactive_color
        self.textColor
