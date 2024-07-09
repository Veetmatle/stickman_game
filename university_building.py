from buildings import Buildings
import pygame as py
import time


class University(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(1571, 675, 33, 29), 'University.png')
        self.study_button = py.Rect(346, 191, 251, 76)
        self.go_to_class_button = py.Rect(346, 295, 252, 80)
        self.go_gym_button = py.Rect(673, 188, 223, 79)
        self.exit_button = py.Rect(674, 473, 141, 78)

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
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.go_gym_button.collidepoint(mouse_pos):
            if self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 10 <= 100:
                self.game.home.dim_screen_smooth()
                self.game.stickman.strength += 1
                self.game.stickman.tiredness += 10
                self.game.stickman.hunger += 10
        elif self.go_to_class_button.collidepoint(mouse_pos):
            if self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 10 <= 100 and self.game.stickman.money - 20 >= 0:
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
            self.exit_building()