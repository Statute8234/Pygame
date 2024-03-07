import pygame
import pygame.sprite
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import random
import pygame_gui
import Map, ColorPicker
# screen
pygame.init()
screenWidth, screenHeight = 600, 600
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
pygame.display.flip()
# color
def RANDOM_COLOR():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
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
        global running, show_pauseMenu, show_mainmenu, show_playerProfile
        pygame_widgets.update(event)
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
                        if button.text == "New Game":
                            show_playerProfile = True
                        show_pauseMenu = False
                        show_mainmenu = False
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
mainMenu = Menu(screen)
# Pause Menu
class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title = Text("Pause", 100, BLACK, (50, 50))
        self.buttons = [Button(50,120,200,50,"Resume",RED,BLACK),
                        Button(50,180,200,50,"Options",RED,BLACK),
                        Button(50,240,200,50,"Restart",RED,BLACK),
                        Button(50,300,200,50,"Quit",RED,BLACK)]
        self.backButton = Button(100,120,50,50,"Back",RED,BLACK)
        self.showSettings = False
        self.showLoadScreen = False
        self.settings()

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

    def handle_event(self, event):
        global running, show_mainmenu, show_pauseMenu, restart
        pygame_widgets.update(event)
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
                    if button.text == "Quit":
                        show_pauseMenu = False
                        show_mainmenu = True
                    if button.text == "Restart":
                        restart = True
                        show_pauseMenu = False
                    if button.text == "Options":
                        self.showSettings = True
                    if button.text == "Resume":
                        show_pauseMenu = False
                    button.reset()
pauseMenu = PauseMenu(screen)
# player Menu
class PlayerMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title = Text("Create Player", 100, BLACK, (50, 20))
        self.name = Text("Name", 36, BLACK, (100, 120))
        self.input_box = pygame.Rect(100, 150, 140, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.flag = Text("Flag Color", 36, BLACK, (100, 200))
        self.flag_color = ColorPicker.ColorPicker(100, 230, 200, 30)
        self.ship = Text("Ship Color", 36, BLACK, (100, 300))
        self.ship_color = ColorPicker.ColorPicker(100, 330, 200, 30)
        self.base = Text("Base Color", 36, BLACK, (100, 400))
        self.base_color = ColorPicker.ColorPicker(100, 430, 200, 30)
        self.submit = Button(100, 500, 100, 50, "Submit",RED, BLACK)
        self.active = False
        self.text = ''
        self.done = False
    
    def draw(self):
        global flagColor, shipColor, baseColor, line
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        self.screen.blit(text_surface, (self.input_box.x+5, self.input_box.y+5))
        self.title.render(screen)
        self.name.render(screen)
        self.flag.render(screen)
        self.flag_color.draw(screen)
        self.playerFlag = pygame.draw.rect(screen, self.flag_color.get_color(), (400, 230, 50, 50))
        flagColor = self.flag_color.get_color()
        self.ship.render(screen)
        self.ship_color.draw(screen)
        self.playerShip = pygame.draw.rect(screen, self.ship_color.get_color(), (400, 330, 100, 50))
        self.base.render(screen)
        self.base_color.draw(screen)
        self.playerShip = pygame.draw.circle(screen, self.base_color.get_color(), (420, 430), 25, 2)
        baseColor = self.base_color.get_color()
        line = Map.Line(baseColor)
        self.submit.draw(screen)

    def update(self):
        width = max(200, self.font.size(self.text)[0]+10)
        self.input_box.w = width
    
    def handle_event(self, event):
        global show_playerProfile
        self.flag_color.update()
        self.ship_color.update()
        self.base_color.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.done = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 9:
                        self.text += event.unicode
        self.submit.handle_event(event)
        if self.submit.clicked:
            show_playerProfile = False
            self.submit.reset()
flagColor, shipColor, baseColor = BLACK, BLACK, BLACK
playerMenu = PlayerMenu(screen)
# functions
def restartMap():
    global stars, show_playerProfile, line, flagColor, shipColor, baseColor
    flagColor, shipColor, baseColor = BLACK, BLACK, BLACK
    stars = []
    line = Map.Line(baseColor)
    for i in range(2,100):
        current_star = Map.Star(random.randint(20,screenWidth - 20),random.randint(20,screenHeight - 20),10,RANDOM_COLOR(),Map.generate_random_string(3),BLACK, RED)
        if current_star.collider(stars) == False:
            stars.append(current_star)
    show_playerProfile = True

def random_star_color():
    color_ranges = [
        (1, (255, 138, 0)),   # Red
        (2, (255, 255, 165)), # Yellow
        (3, (255, 255, 255)), # White
        (4, (170, 191, 255)),# Blue-white
        (5, (94, 166, 255))  # Blue
    ]
    # Choose a random temperature within the defined range
    min_temp, max_temp = color_ranges[0][0], color_ranges[-1][0]
    temperature = random.randint(min_temp, max_temp)
    for temp, color in color_ranges:
        if temperature <= temp:
            return color
    return (94, 166, 255)
# map
stars = []
for i in range(2,100):
    current_star = Map.Star(random.randint(20,screenWidth - 20),random.randint(20,screenHeight - 20),5,random_star_color(),Map.generate_random_string(4),WHITE, RED)
    if current_star.collider(stars) == False:
        stars.append(current_star)
line = Map.Line(baseColor)
# loop
running = True
show_mainmenu = True
show_pauseMenu = False
show_playerProfile = False
restart = False
def main():
    global running, show_mainmenu, show_pauseMenu, restart, screenWidth, screenHeight
    while running:
        mousePos = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                line.remove_intersecting_segment(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and show_mainmenu == False:
                    show_pauseMenu = not(show_pauseMenu)
            elif event.type == pygame.VIDEORESIZE:
                screenWidth, screenHeight = event.size
            if show_mainmenu:
                mainMenu.handle_event(event)
            if show_pauseMenu:
                pauseMenu.handle_event(event)
            playerMenu.handle_event(event)
            # stars
            for star in stars:
                star.handle_events(event)
                star.highlight(mousePos)
                if star.clicked:
                    star.text_color = flagColor
                    line.add_point(star.x, star.y)
                    star.reset()
        screen.fill(WHITE)
        if show_mainmenu:
            mainMenu.update(screenWidth, screenHeight)
            mainMenu.draw()
        elif show_pauseMenu:
            pauseMenu.update(screenWidth, screenHeight)
            pauseMenu.draw()
        elif restart:
            restartMap()
            restart = False
        elif show_playerProfile:
            playerMenu.draw()
        # game
        else:
            screen.fill(BLACK)
            line.draw(screen)
            for star in stars:
                star.draw(screen)
        # update
        pygame.display.flip()
        pygame.display.update()
        clock.tick(64)

if __name__ == "__main__":
    main()
