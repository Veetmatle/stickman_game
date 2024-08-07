import pygame as py
import time
from buildings import Buildings


class MCDonald(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(835, 679, 25, 55), 'images/mcd.png')
        self.milkshake_button = py.Rect(346, 207, 325, 76)
        self.fries_button = py.Rect(343, 307, 288, 69)
        self.cheeseburger_button = py.Rect(345, 405, 226, 70)
        self.triple_burger_button = py.Rect(344, 503, 229, 70)
        self.mcd_work_button = py.Rect(677, 305, 198, 71)
        self.leave_button = py.Rect(676, 501, 145, 72)

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.milkshake_button.collidepoint(mouse_pos):
            self.message = "Click to have a milkshake"
        elif self.fries_button.collidepoint(mouse_pos):
            self.message = "Click to have some fries"
        elif self.cheeseburger_button.collidepoint(mouse_pos):
            self.message = "Click to eat cheeseburger"
        elif self.triple_burger_button.collidepoint(mouse_pos):
            self.message = "Click to eat triple burger"
        elif self.mcd_work_button.collidepoint(mouse_pos):
            self.message = "Click to work"
        elif self.leave_button.collidepoint(mouse_pos):
            self.message = "Click to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.milkshake_button.collidepoint(mouse_pos):
            if self.game.stickman.money - 8 >= 0:
                self.game.stickman.money -= 8
                self.game.home.dim_screen_smooth()
                if self.game.stickman.hunger - 10 >= 0:
                    self.game.stickman.hunger -= 10
                else:
                    self.game.stickman.hunger = 0
        elif self.fries_button.collidepoint(mouse_pos):
            if self.game.stickman.money - 12 >= 0:
                self.game.stickman.money -= 12
                self.game.home.dim_screen_smooth()
                if self.game.stickman.hunger - 15 >= 0:
                    self.game.stickman.hunger -= 15
                else:
                    self.game.stickman.hunger = 0
        elif self.cheeseburger_button.collidepoint(mouse_pos):
            if self.game.stickman.money - 25 >= 0:
                self.game.stickman.money -= 25
                self.game.home.dim_screen_smooth()
                if self.game.stickman.hunger - 35 >= 0:
                    self.game.stickman.hunger -= 35
                else:
                    self.game.stickman.hunger = 0
        elif self.triple_burger_button.collidepoint(mouse_pos):
            if self.game.stickman.money - 50 >= 0:
                self.game.home.dim_screen_smooth()
                self.game.stickman.money -= 50
                if self.game.stickman.hunger - 70 >= 0:
                    self.game.stickman.hunger -= 70
                else:
                    self.game.stickman.hunger = 0
        elif self.mcd_work_button.collidepoint(mouse_pos):
            if self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 4 <= 100:
                self.game.stickman.money += 6
                self.game.stickman.tiredness += 10
                self.game.stickman.hunger += 4
                self.game.stickman.update_experience(50)
                hours, minutes = map(int, self.game.stickman.clock.split(':'))
                hours += 1
                if hours >= 24:
                    hours %= 24
                    self.game.stickman.days += 1
                self.game.stickman.clock = f"{hours:02d}:{minutes:02d}"
        elif self.leave_button.collidepoint(mouse_pos):
            self.exit_building()
