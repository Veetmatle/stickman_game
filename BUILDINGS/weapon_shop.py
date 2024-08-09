import pygame as py
from BUILDINGS.buildings import Buildings


class WeaponShop(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(1133, 1386, 32, 51), "images/weapon_store.jpg")
        self.buy_knife_button = py.Rect(12, 38, 235, 469)
        self.buy_axes_button = py.Rect(275, 36, 234, 473)
        self.buy_pistol_button = py.Rect(537, 38, 229, 474)
        self.buy_bazooka_button = py.Rect(797, 38, 201, 472)
        self.exit_button = py.Rect(558, 724, 178, 59)

        self.knife_bought = False
        self.axes_bought = False
        self.pistol_bought = False
        self.bazooka_bought = False

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.buy_knife_button.collidepoint(mouse_pos):
            if self.game.stickman.money >= 200 and not self.knife_bought:
                self.message = "Click to buy knife"
            elif self.knife_bought:
                self.message = "You already bought knife"
            else:
                self.message = "No money for knife"

        elif self.buy_axes_button.collidepoint(mouse_pos):
            if self.game.stickman.money >= 500 and not self.axes_bought:
                self.message = "Click to buy axes"
            elif self.axes_bought:
                self.message = "You already bought axes"
            else:
                self.message = "No money for axes"

        elif self.buy_pistol_button.collidepoint(mouse_pos):
            if self.game.stickman.money >= 500 and not self.pistol_bought:
                self.message = "Click to buy pistol"
            elif self.pistol_bought:
                self.message = "You already bought pistol"
            else:
                self.message = "No money for pistol"

        elif self.buy_bazooka_button.collidepoint(mouse_pos):
            if self.game.stickman.money >= 1000 and not self.bazooka_bought:
                self.message = "Click to buy bazooka"
            elif self.bazooka_bought:
                self.message = "You already bought bazooka"
            else:
                self.message = "No money for bazooka"

        elif self.exit_button.collidepoint(mouse_pos):
            self.message = "Click to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.buy_knife_button.collidepoint(mouse_pos) and not self.knife_bought and self.game.stickman.money >= 200:
            self.game.stickman.money -= 200
            self.knife_bought = True
            self.game.stickman.strength += 30
            self.game.stickman.update_experience(100)

        elif self.buy_axes_button.collidepoint(mouse_pos) and not self.axes_bought and self.game.stickman.money >= 500:
            self.game.stickman.money -= 500
            self.axes_bought = True
            self.game.stickman.strength += 60
            self.game.stickman.update_experience(300)

        elif self.buy_pistol_button.collidepoint(mouse_pos) and not self.pistol_bought and self.game.stickman.money >= 500:
            self.game.stickman.money -= 500
            self.pistol_bought = True
            self.game.stickman.strength += 60
            self.game.stickman.update_experience(300)

        elif self.buy_bazooka_button.collidepoint(mouse_pos) and not self.bazooka_bought and self.game.stickman.money >= 1000:
            self.game.stickman.money -= 1000
            self.bazooka_bought = True
            self.game.stickman.strength += 60
            self.game.stickman.update_experience(500)

        elif self.exit_button.collidepoint(mouse_pos):
            self.exit_building()
