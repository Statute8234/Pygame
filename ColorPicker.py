import pygame

import pygame

import pygame

class ColorPicker:
    def __init__(self, x, y, w, h):
        # Initialize the ColorPicker with a rectangle and an image
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 255, 255))  # Fill the image with white
        self.rad = h // 2  # Radius of the circle
        self.pwidth = w - self.rad * 2  # Width of the color spectrum
        self.selected_color = (0, 0, 0)  # Initialize selected color to black
        # Create the color spectrum on the image
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360 * i / self.pwidth), 100, 50, 100)
            pygame.draw.rect(self.image, color, (i + self.rad, h // 3, 1, h - 2 * h // 3))
        self.p = 0  # Initial position of the picker

    def get_color(self):
        # Get the color at the current position of the picker
        color = pygame.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        return color

    def update(self):
        # Update the position of the picker based on mouse input
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = max(0, min(self.p, 1))  # Ensure picker position stays within bounds
            self.selected_color = self.get_color()

    def draw(self, surf):
        # Draw the color picker on the specified surface
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_color(), center, self.rect.height // 2)
