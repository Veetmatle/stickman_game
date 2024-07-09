import pygame as py

class University(object):
    def __init__(self, game):
        self.game = game
        self.entered = False
        self.uni_entry_rect = py.Rect(1571, 675, 33, 29)
        self.uni_image = py.image.load('University.png').convert()
        self.able_to_enter = False
        # buttons inside
        self.study_button = py.Rect(346, 191, 251, 76)
        self.go_to_class_button = py.Rect(346, 295, 252, 80)
        self.go_gym_button = py.Rect(673, 188, 223, 79)
        self.exit_button = py.Rect(674, 473, 141, 78)
        self.message = ""

    def enter_the_uni(self):
        if self.able_to_enter and not self.entered:
            self.entered = True
            self.able_to_enter = False
            self.game.stickman.active = False
            py.mouse.set_visible(True)
            # Change the background to the home image
            uni_image_scaled = py.transform.scale(self.uni_image, self.game.window_size)
            self.game.screen.blit(uni_image_scaled, (0, 0))
            py.display.flip()

    def update(self):
        if self.entered:
            self.handle_buttons()
            uni_image_scaled = py.transform.scale(self.uni_image, self.game.window_size)
            self.game.screen.blit(uni_image_scaled, (0, 0))
            self.game.stickman.draw_properties()
            if self.message:
                font = py.font.SysFont(None, 24)
                text = font.render(self.message, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] - 30))
                self.game.screen.blit(text, text_rect)
                self.game.stickman.draw_properties()
            py.display.flip()

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.study_button.collidepoint(mouse_pos):
            self.message = "Click to study"
        elif self.go_to_class_button.collidepoint(mouse_pos):
            self.message = "Go to class"
        elif self.exit_button.collidepoint(mouse_pos):
            self.message = "Click to exit"
        elif self.go_gym_button.collidepoint(mouse_pos):
            self.message = "Go to gym"

        if self.message != previous_message:
            uni_image_scaled = py.transform.scale(self.uni_image, self.game.window_size)
            self.game.screen.blit(uni_image_scaled, (0, 0))

    def handle_uni_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.game.running = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.exit_the_home()
                elif event.key == py.K_e:
                    self.enter_the_uni()
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = py.mouse.get_pos()
                    if self.go_gym_button.collidepoint(mouse_pos):
                        if self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 10 <= 100:
                            self.game.home.dim_screen_smooth()
                            self.game.stickman.strength += 1
                            self.game.stickman.tiredness += 10
                            self.game.stickman.hunger += 10
                    elif self.go_to_class_button.collidepoint(mouse_pos):
                        if self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 10 <= 100:
                            self.game.home.dim_screen_smooth()
                            self.game.stickman.intellect += 2
                            self.game.stickman.tiredness += 10
                            self.game.stickman.hunger += 10
                            self.game.stickman.money -= 20
                    elif self.study_button.collidepoint(mouse_pos):
                        if self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 5 <= 100:
                            self.game.home.dim_screen_smooth()
                            self.game.stickman.intellect += 1
                            self.game.stickman.tiredness += 10
                            self.game.stickman.hunger += 5
                    elif self.exit_button.collidepoint(mouse_pos):
                        self.exit_the_home()

    def draw_enter_message(self):
        if not self.entered:
            self.able_to_enter = True
            font = py.font.SysFont(None, 24)
            text = font.render("Press 'E' to enter", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] - 30))
            self.game.screen.blit(text, text_rect)

    def exit_the_home(self):
        if self.entered:
            self.entered = False
            self.game.stickman.active = True
            py.mouse.set_visible(False)
            self.message = ""
