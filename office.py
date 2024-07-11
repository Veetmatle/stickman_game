import pygame as py
from buildings import Buildings


class Office(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(1132, 513, 24, 63), 'biuro.png')
        self.work_intern_button = py.Rect(270, 394, 317, 64)
        self.work_senior_button = py.Rect(272, 473, 318, 73)
        self.work_manager_button = py.Rect(270, 558, 342, 74)
        self.exit_button = py.Rect(699, 571, 142, 56)

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.work_intern_button.collidepoint(mouse_pos):
            self.message = "Click to work intern"
        elif self.work_senior_button.collidepoint(mouse_pos):
            self.message = "Click to work senior"
        elif self.work_manager_button.collidepoint(mouse_pos):
            self.message = "Click to work manager"
        elif self.exit_button.collidepoint(mouse_pos):
            self.message = "Click to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.work_intern_button.collidepoint(mouse_pos):
            if self.game.stickman.intellect >= 40 and self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 6 <= 100:
                self.game.stickman.money += 15
                self.game.stickman.tiredness += 10
                self.game.stickman.hunger += 6
                self.game.stickman.update_experience(75)
                hours, minutes = map(int, self.game.stickman.clock.split(':'))
                hours += 1
                if hours >= 24:
                    hours %= 24
                    self.game.stickman.days += 1
                self.game.stickman.clock = f"{hours:02d}:{minutes:02d}"


        elif self.work_senior_button.collidepoint(mouse_pos):
            if self.game.stickman.intellect >= 70 and self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 6 <= 100:
                self.game.stickman.money += 25
                self.game.stickman.tiredness += 10
                self.game.stickman.hunger += 6
                self.game.stickman.update_experience(100)
                hours, minutes = map(int, self.game.stickman.clock.split(':'))
                hours += 1
                if hours >= 24:
                    hours %= 24
                    self.game.stickman.days += 1
                self.game.stickman.clock = f"{hours:02d}:{minutes:02d}"

        elif self.work_manager_button.collidepoint(mouse_pos):
            if self.game.stickman.intellect >= 115 and self.game.stickman.tiredness + 10 <= 100 and self.game.stickman.hunger + 6 <= 100:
                self.game.stickman.money += 50
                self.game.stickman.tiredness += 10
                self.game.stickman.hunger += 6
                self.game.stickman.update_experience(150)
                hours, minutes = map(int, self.game.stickman.clock.split(':'))
                hours += 1
                if hours >= 24:
                    hours %= 24
                    self.game.stickman.days += 1
                self.game.stickman.clock = f"{hours:02d}:{minutes:02d}"

        elif self.exit_button.collidepoint(mouse_pos):
            self.exit_building()
