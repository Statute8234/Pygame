import pygame
import random, sys, time
import math

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

    def rotate(self, mouse_pos):
        if self.active:
            rel_mouse_x, rel_mouse_y = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
            self.angle = (180 / math.pi) * -math.atan2(rel_mouse_y, rel_mouse_x)
            self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (self.width, self.height)), self.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)
    
    def move(self, newPosition):
        if self.active:
            self.rect.center = newPosition

    def deactivePlayer(self, screen):
        self.deactiveOriginal_image = pygame.image.load(self.deactiveImage).convert_alpha()
        self.deactive_image = pygame.transform.scale(self.deactiveOriginal_image, (self.width, self.height))
        screen.blit(self.deactive_image, (self.rect.centerx - self.width / 2,self.rect.centery - self.height / 2))

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
