import pygame as py
from buildings import Buildings


class DrugStore(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(1134, 1110, 24, 74), "drug_store.jpg")
        self.buy_cigarettes_button = py.Rect(290, 123, 262, 55)
        self.buy_vodka_button = py.Rect(284, 180, 271, 51)
        self.buy_drugs_button = py.Rect(569, 115, 265, 119)
        self.exit_button = py.Rect(226, 624, 568, 64)

        self.drugs_bought = False
        self.alcohol_bought = False
        self.cigarettes_bought = False

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.buy_cigarettes_button.collidepoint(mouse_pos):
            if self.game.stickman.money >= 200 and not self.cigarettes_bought:
                self.message = "Click to buy cigarettes"
            elif self.cigarettes_bought:
                self.message = "You already bought cigarettes."
            else:
                self.message = "Not enough money to buy cigarettes."

        elif self.buy_vodka_button.collidepoint(mouse_pos):
            if self.game.stickman.money >= 200 and not self.alcohol_bought:
                self.message = "Click to buy vodka"
            elif self.alcohol_bought:
                self.message = "You already bought alcohol."
            else:
                self.message = "Not enough money to buy vodka."

        elif self.buy_drugs_button.collidepoint(mouse_pos):
            if self.game.stickman.money >= 1000 and not self.drugs_bought:
                self.message = "Click to buy drugs"
            elif self.drugs_bought:
                self.message = "You already bought drugs."
            else:
                self.message = "Not enough money to buy drugs."

        elif self.exit_button.collidepoint(mouse_pos):
            self.message = "Click to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.buy_cigarettes_button.collidepoint(mouse_pos) and self.game.stickman.money >= 200 and not self.cigarettes_bought:
            self.cigarettes_bought = True
            self.game.stickman.money -= 200
            self.game.stickman.update_experience(100)
        elif self.buy_vodka_button.collidepoint(mouse_pos) and self.game.stickman.money >= 200 and not self.alcohol_bought:
            self.alcohol_bought = True
            self.game.stickman.update_experience(200)
            self.game.stickman.money -= 200
        elif self.buy_drugs_button.collidepoint(mouse_pos) and self.game.stickman.money >= 1000 and not self.drugs_bought:
            self.drugs_bought = True
            self.game.stickman.update_experience(800)
            self.game.stickman.money -= 1000
        elif self.exit_button.collidepoint(mouse_pos):
            self.exit_building()
