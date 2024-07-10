import pygame as py
from buildings import Buildings


class Hospital(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(445, 622, 50, 30), 'hospital.png')
        self.heal_yourself_button = py.Rect(375, 300, 293, 56)
        self.satisfy_hunger_button = py.Rect(380, 385, 247, 59)
        self.satisfy_tiredness_button = py.Rect(380, 470, 272, 61)
        self.exit_button = py.Rect(800, 475, 140, 57)

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.heal_yourself_button.collidepoint(mouse_pos):
            self.message = "Click to heal yourself"
        elif self.satisfy_hunger_button.collidepoint(mouse_pos):
            self.message = "Click to satisfy hunger"
        elif self.satisfy_tiredness_button.collidepoint(mouse_pos):
            self.message = "Click to satisfy tiredness"
        elif self.exit_button.collidepoint(mouse_pos):
            self.message = "Click to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.heal_yourself_button.collidepoint(mouse_pos):
            if self.game.stickman.money - 250 >= 0:
                self.game.stickman.money -= 250
                self.game.stickman.hp = 1000
        elif self.satisfy_tiredness_button.collidepoint(mouse_pos):
            if self.game.stickman.experience - 250 >= 0:
                self.game.stickman.update_experience(-250)
                self.game.stickman.tiredness = 0
            elif self.game.stickman.level > 1 and self.game.stickman.experience - 250 < 0:
                self.game.stickman.level -= 1
                self.game.stickman.update_experience(750)
                self.game.stickman.tiredness = 0
        elif self.satisfy_hunger_button.collidepoint(mouse_pos):
            if self.game.stickman.experience - 500 >= 0:
                self.game.stickman.update_experience(-500)
                self.game.stickman.hunger = 0
            elif self.game.stickman.level > 1 and self.game.stickman.experience - 500 < 0:
                self.game.stickman.level -= 1
                self.game.stickman.update_experience(500)
                self.game.stickman.hunger = 0
        elif self.exit_button.collidepoint(mouse_pos):
            self.exit_building()



