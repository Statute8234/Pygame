import pygame
import pygame.sprite
import sys
import pygame_widgets
from pygame.surfarray import make_surface
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
# screen
pygame.init()
screenWidth, screenHeight = 600, 600
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
pygame.display.flip()
# color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
# text
class Text:
    def __init__(self, text, font_size, color, position):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.position = position
        self.font = pygame.font.Font(None, self.font_size)  # You can specify a font file or use None for default font
        self.rendered_text = None

    def update(self, new_text):
        self.text = new_text
        self.rendered_text = None  # Clear the rendered text to update it

    def render(self, screen):
        if self.rendered_text is None:
            self.rendered_text = self.font.render(self.text, True, self.color)
        screen.blit(self.rendered_text, self.position)
# button
class Button:
    def __init__(self, x, y, width, height, text, active_color, inactive_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.textColor = BLACK
        self.font_size = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.font_size)
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 2)
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.color = self.active_color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
                    self.color = self.active_color
        else:
            self.color = self.inactive_color
    def reset(self):
        self.clicked = False
        self.color = self.inactive_color
# menu
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.title = Text("Menu", 100, BLACK, (50, 50))
        self.buttons = [Button(50,120,200,50,"New Game",RED,BLACK),
                        Button(50,180,200,50,"Load Game",RED,BLACK),
                        Button(50,240,200,50,"continue",RED,BLACK),
                        Button(50,300,200,50,"Options",RED,BLACK),
                        Button(50,360,200,50,"Exit",RED,BLACK)]
        self.backButton = Button(100,120,50,50,"Back",RED,BLACK)
        self.showSettings = False
        self.showLoadScreen = False
        self.settings()
        self.loadScreen()

    def loadScreen(self):
        self.loadSlots = [Button(50, (x * 60) + 200, 200, 50, "Slot", RED, BLACK) for x in range(5)]
        
    def settings(self):
        self.sound = Text("Music", 36, BLACK, (230, 200))
        self.sound_slider = Slider(screen, 230, 240, 200, 10, min=0, max=100, step=1, initial=100)
        self.sound_output = TextBox(screen, 440, 210, 50, 50, fontSize=25)
        self.sound_output.disable()
        self.sound_effects = Text("Sound Effects", 36, BLACK, (230, 300))
        self.sound_effects_slider = Slider(screen, 230, 340, 200, 10, min=0, max=100, step=1, initial=100)
        self.sound_effects_output = TextBox(screen, 440, 310, 50, 50, fontSize=25)
        self.sound_effects_output.disable()
        self.frame_rate = Text("Frame Rate", 36, BLACK, (230, 400))
        self.frame_rate_slider = Slider(screen, 230, 450, 128, 10, min=1, max=64, step=1, initial=64)
        self.frame_rate_output = TextBox(screen, 440, 413, 50, 50, fontSize=25)
        self.frame_rate_output.disable()
        self.brightness_text = Text("Brightness", 36, BLACK, (230, 500))
        self.brightness_slider = Slider(screen, 230, 550, 200, 10, min=0, max=1.0, step=0.1, initial=1.0)
        self.brightness_output = TextBox(screen, 440, 513, 50, 50, fontSize=25)
        self.brightness_output.disable()

    def draw(self):
        self.screen.fill(WHITE)
        if self.showSettings == False and self.showLoadScreen == False:
            for button in self.buttons:
                button.draw(self.screen)
        self.title.render(screen)
        # load game
        if (self.showLoadScreen):
            self.backButton.draw(screen)
            for loadSlot in self.loadSlots:
                loadSlot.draw(screen)

        # settings
        if (self.showSettings):
            self.backButton.draw(screen)
            self.sound.render(screen)
            self.sound_slider.draw()
            self.sound_output.draw()
            self.sound_output.setText(self.sound_slider.getValue())

            self.sound_effects.render(screen)
            self.sound_effects_slider.draw()
            self.sound_effects_output.draw()
            self.sound_effects_output.setText(self.sound_effects_slider.getValue())

            self.frame_rate.render(screen)
            self.frame_rate_slider.draw()
            self.frame_rate_output.draw()
            self.frame_rate_output.setText(self.frame_rate_slider.getValue())

            self.brightness_text.render(screen)
            self.brightness_slider.draw()
            self.brightness_output.draw()
            self.brightness_output.setText(round(self.brightness_slider.getValue(),2))

    def update(self, screenHeight, screenWidth):
        self.title.position = ((screenHeight / 2) - 100, 50)

        button_x = (screenHeight / 2) - 100
        for button in self.buttons:
            button.x = button_x
        # loadslot
        for loadSlot in self.loadSlots:
            loadSlot.x = button_x

    def handle_event(self, event):
        global running, Mainmenu, playGame
        pygame_widgets.update(event)
        if Mainmenu == False:
            self.backButton.handle_event(event)
            if self.backButton.clicked:
                if self.showSettings:
                    self.showSettings = False
                else:
                    self.showLoadScreen = False
                self.backButton.reset()
            # others
            if self.showSettings == False and self.showLoadScreen == False:
                for button in self.buttons:
                    button.handle_event(event)
                    if button.color == button.active_color:
                        button.textColor = button.active_color
                    else:
                        button.textColor = button.inactive_color
                    if button.clicked:
                        if button.text == "Exit":
                            running = False
                            sys.exit()
                        if button.text == "continue" or button.text == "New Game":
                            Mainmenu = False
                            playGame = True
                        if button.text == "Options":
                            self.showSettings = True
                        if button.text == "Load Game":
                            self.showLoadScreen = True
                        button.reset()
            # loadslot
            for loadSlot in self.loadSlots:
                loadSlot.handle_event(event)
                if loadSlot.color == loadSlot.active_color:
                    loadSlot.textColor = loadSlot.active_color
                else:
                    loadSlot.textColor = loadSlot.inactive_color
                if loadSlot.clicked:
                    loadSlot.reset()
menu = Menu(screen)
# play menu

# loop
running = True
Mainmenu = True
playGame = False
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playGame = not(playGame)
        elif event.type == pygame.VIDEORESIZE:
            screenWidth, screenHeight = event.size
        menu.handle_event(event)

    screen.fill(WHITE)
    if Mainmenu:
        menu.update(screenWidth, screenHeight)
        menu.draw()
    if playGame:

    # update
    pygame.display.flip()
    pygame.display.update()
    clock.tick(64)
