from buildings import Buildings
import pygame as py
import time


class Home(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(324, 267, 51, 90), 'dom_stickman.png')
        self.message_button = py.Rect(358, 404, 286, 79)
        self.sleep_button = py.Rect(361, 516, 151, 80)
        self.leave_button = py.Rect(792, 514, 160, 80)
        self.pay_bills_button = py.Rect(365, 293, 294, 79)
        self.bills_paid = True

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""
        if self.bills_paid and not self.leave_button.collidepoint(mouse_pos) and not self.pay_bills_button.collidepoint(mouse_pos):
            if self.message_button.collidepoint(mouse_pos):
                self.message = "Click to check messages"
            elif self.sleep_button.collidepoint(mouse_pos):
                self.message = "Click to sleep"
        elif not self.bills_paid and not self.leave_button.collidepoint(mouse_pos) and not self.pay_bills_button.collidepoint(mouse_pos):
            self.message = "Pay the bills to continue."
        elif self.leave_button.collidepoint(mouse_pos):
            self.message = "Click to exit"
        elif self.pay_bills_button.collidepoint(mouse_pos):
            self.message = "Click to pay bills"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.message_button.collidepoint(mouse_pos) and self.bills_paid:
            print("Check messages button clicked")
        elif self.sleep_button.collidepoint(mouse_pos) and self.bills_paid:
            self.dim_screen_smooth()
            self.game.stickman.tiredness = 0
            hours, minutes = map(int, self.game.stickman.clock.split(':'))
            hours += 8
            if hours >= 24:
                hours %= 24
                self.game.stickman.days += 1
            self.game.stickman.clock = f"{hours:02d}:{minutes:02d}"
        elif self.pay_bills_button.collidepoint(mouse_pos) and not self.bills_paid:
            if self.game.stickman.money - 100 >= 0:
                self.game.stickman.money -= 100
                self.bills_paid = True
                self.game.stickman.last_bills_paid_day = self.game.stickman.days
        elif self.leave_button.collidepoint(mouse_pos):
            self.exit_building()

    def draw(self):
        if not self.bills_paid:
            self.draw_bills_message()

    def draw_bills_message(self):
        x = self.game.window_size[0] // 2
        y = self.game.window_size[1] - 20
        font = py.font.SysFont(None, 24)
        text = font.render('Pay the bills to continue', True, (255, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        self.game.screen.blit(text, text_rect)

