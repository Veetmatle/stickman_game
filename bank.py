import pygame as py
from buildings import Buildings


class Bank(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(1134, 307, 21, 48), "bank.jpg")
        self.work_button = py.Rect(63, 479, 261, 264)
        self.rob_button = py.Rect(375, 480, 254, 266)
        self.take_loan_button = py.Rect(684, 480, 266, 276)

        self.bank_robbed = False

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.work_button.collidepoint(mouse_pos):
            if self.game.stickman.intellect >= 200 and not self.bank_robbed:
                self.message = "Click to work, 100$/h"
            elif self.bank_robbed:
                self.message = "You can't work here, you robbed the bank"
            else:
                self.message = "You need 200 intellect to work here"

        elif self.rob_button.collidepoint(mouse_pos):
            if self.game.stickman.strength >= 200 and not self.bank_robbed:
                self.message = "Click to rob the bank"
            elif self.bank_robbed:
                self.message = "You have already robbed the bank"
            else:
                self.message = "You need 200 strength to rob bank"

        elif self.take_loan_button.collidepoint(mouse_pos):
            if self.game.stickman.popularity >= 200:
                self.message = "Click to take loan"
            else:
                self.message = "You need 200 popularity to take loan"
        else:
            self.message = "Click esc to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.work_button.collidepoint(mouse_pos):
            if self.game.stickman.intellect >= 200 and self.game.stickman.tiredness + 15 <= 100 and self.game.stickman.hunger + 15 <= 100 and not self.bank_robbed:
                self.game.stickman.money += 100
                self.game.stickman.tiredness += 15
                self.game.stickman.hunger += 15
                if self.game.stickman.level < 15:
                    self.game.stickman.update_experience(200)
                    hours, minutes = map(int, self.game.stickman.clock.split(':'))
                    hours += 1
                if hours >= 24:
                    hours %= 24
                    self.game.stickman.days += 1
                self.game.stickman.clock = f"{hours:02d}:{minutes:02d}"

        if self.rob_button.collidepoint(mouse_pos) and self.game.stickman.strength >= 200 and not self.bank_robbed:
            self.game.home.dim_screen_smooth()
            self.game.stickman.strength -= 50
            if self.game.stickman.level >= 5:
                    self.game.stickman.level -= 5
            else:
                self.game.stickman.level = 0
            self.game.stickman.experience = 0
            self.game.stickman.popularity = 0
            self.game.stickman.money += 3000
            self.bank_robbed = True


