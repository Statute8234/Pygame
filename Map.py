import pygame
import pygame.sprite
import sys
import pygame_widgets
from pygame.surfarray import make_surface
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import math, string, random

# make a random string
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Star
class Star:
    def __init__(self, x, y, radius, color, text, text_color, highlight_color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.default_color = color
        self.highlight_color = highlight_color
        self.text = text
        self.text_color = text_color
        self.highlighted = False
        self.clicked = False
        self.owned = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        if self.text and self.highlighted:
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x, self.y - 20))
            screen.blit(text_surface, text_rect)

    def highlight(self, mouse_pos):
        distance = math.sqrt((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2)
        self.highlighted = distance <= self.radius
        if self.highlighted:
            self.color = self.highlight_color
        else:
            self.color = self.default_color

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.highlighted:
                    self.clicked = True
                    self.owned = True

    def collider(self, other_stars):
        for other_star in other_stars:
            if other_star != self:
                distance = math.sqrt((other_star.x - self.x) ** 2 + (other_star.y - self.y) ** 2)
                if distance < (self.radius + other_star.radius):
                    return True
        return False
    
    def reset(self):
        self.clicked = False
# lines
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, color):
        self.points = []
        self.color = color

    def add_point(self, x, y):
        new_point = Point(x, y)
        self.points.append(new_point)

    def draw(self, screen):
        for i in range(len(self.points) - 1):
            pygame.draw.line(screen, self.color, (self.points[i].x, self.points[i].y), (self.points[i + 1].x, self.points[i + 1].y), 2)

    def remove_intersecting_segment(self, mouse_pos):
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            p1p2 = pygame.Rect(min(p1.x, p2.x), min(p1.y, p2.y), abs(p1.x - p2.x), abs(p1.y - p2.y))
            if p1p2.collidepoint(mouse_pos):
                del self.points[i + 1]
                return True
        return False
