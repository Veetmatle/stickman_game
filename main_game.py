import sys
import pygame as py
from stickman_player import StickMan
from home_building import Home
from university_building import University
from MCdonalds import MCDonald
from hospital import Hospital
from office import Office
from castle import Castle
from drug_store import DrugStore
from weapon_shop import WeaponShop
from bank import Bank

class Game:
    def __init__(self):
        """
        Initializes the Game class, setting up the basic game parameters such as
        window size, map size, background, collision mask, and initializes the
        player and building objects.
        """
        py.init()
        self.window_size = (1000, 800)  # Size of the camera
        self.map_size = (2048, 1732)  # Main map size
        self.screen = py.display.set_mode(self.window_size)
        py.display.set_caption('StickMan Jr')
        self.clock = py.time.Clock()
        self.running = True

        # Load background image
        self.background = py.image.load('game_background.png').convert()

        # Load collision mask
        collision_mask_image = py.image.load('maska.png').convert()
        self.collision_mask = py.mask.from_threshold(collision_mask_image, (255, 255, 255), (1, 1, 1, 255))

        # Initialize StickMan (player character)
        self.stickman = StickMan(self)

        # Initialize buildings
        self.home = Home(self)
        self.university = University(self)
        self.mcd = MCDonald(self)
        self.hospital = Hospital(self)
        self.office = Office(self)
        self.castle = Castle(self)
        self.drug_store = DrugStore(self)
        self.weapon_shop = WeaponShop(self)
        self.bank = Bank(self)

    def run(self):
        """
        Main game loop that keeps the game running. It handles events, updates
        the game state, and draws the current frame. The loop continues until
        the game is quit.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        py.quit()
        sys.exit()

    def handle_events(self):
        """
        Handles user input and game events. Checks if the player has entered a
        building and handles specific events for that building, otherwise processes
        general game events such as quitting the game or interacting with buildings.
        """
        if self.home.entered:
            self.home.handle_events()
        elif self.university.entered:
            self.university.handle_events()
        elif self.mcd.entered:
            self.mcd.handle_events()
        elif self.hospital.entered:
            self.hospital.handle_events()
        elif self.office.entered:
            self.office.handle_events()
        elif self.castle.entered:
            self.castle.handle_events()
        elif self.drug_store.entered:
            self.drug_store.handle_events()
        elif self.weapon_shop.entered:
            self.weapon_shop.handle_events()
        elif self.bank.entered:
            self.bank.handle_events()
        else:
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                elif event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        self.running = False
                    elif event.key == py.K_e and self.home.able_to_enter and self.stickman.rect.colliderect(self.home.entry_rect):
                        self.home.enter_building()
                    elif event.key == py.K_e and self.university.able_to_enter and self.stickman.rect.colliderect(self.university.entry_rect):
                        self.university.enter_building()
                    elif event.key == py.K_e and self.mcd.able_to_enter and self.stickman.rect.colliderect(self.mcd.entry_rect):
                        self.mcd.enter_building()
                    elif event.key == py.K_e and self.hospital.able_to_enter and self.stickman.rect.colliderect(self.hospital.entry_rect):
                        self.hospital.enter_building()
                    elif event.key == py.K_e and self.office.able_to_enter and self.stickman.rect.colliderect(self.office.entry_rect):
                        self.office.enter_building()
                    elif event.key == py.K_e and self.castle.able_to_enter and self.stickman.rect.colliderect(self.castle.entry_rect):
                        self.castle.enter_building()
                    elif event.key == py.K_e and self.drug_store.able_to_enter and self.stickman.rect.colliderect(self.drug_store.entry_rect):
                        self.drug_store.enter_building()
                    elif event.key == py.K_e and self.weapon_shop.able_to_enter and self.stickman.rect.colliderect(self.weapon_shop.entry_rect):
                        self.weapon_shop.enter_building()
                    elif event.key == py.K_e and self.bank.able_to_enter and self.stickman.rect.colliderect(self.bank.entry_rect):
                        self.bank.enter_building()

    def update(self):
        """
        Updates the game state. If the player is not inside any building, it updates
        the player's state and controls time flow. It also checks certain conditions
        in the game, such as those related to the hospital.
        """
        if not (self.home.entered or self.university.entered or self.mcd.entered or self.hospital.entered or self.office.entered
                or self.castle.entered or self.drug_store.entered or self.weapon_shop.entered or self.bank.entered):
            self.stickman.handle_keys()
        if not self.castle.entered:
            self.stickman.control_time_flow()
            self.hospital.check_conditions()

    def draw(self):
        """
        Draws the current game frame. Depending on the player's location, it either
        draws the main map with the player and buildings or updates the display within
        a specific building. It also handles camera movement and UI elements such as
        experience bars and health points.
        """
        if not (self.home.entered or self.university.entered or self.mcd.entered or self.hospital.entered
                or self.office.entered or self.castle.entered or self.drug_store.entered or self.weapon_shop.entered
        or self.bank.entered):
            # Determine camera position
            camera_x = max(0, min(self.stickman.rect.centerx - self.window_size[0] // 2, self.map_size[0] - self.window_size[0]))
            camera_y = max(0, min(self.stickman.rect.centery - self.window_size[1] // 2, self.map_size[1] - self.window_size[1]))
            camera_offset = (-camera_x, -camera_y)

            # Draw the background with camera offset
            self.screen.blit(self.background, camera_offset)
            self.stickman.draw(self.screen, camera_offset)

            # Draw experience bar, level, HP, etc.
            self.stickman.draw_properties()

            # Check if the player is near the entrance of any building
            if self.stickman.rect.colliderect(self.home.entry_rect):
                self.home.draw_enter_message()
            elif self.stickman.rect.colliderect(self.university.entry_rect):
                self.university.draw_enter_message()
            elif self.stickman.rect.colliderect(self.mcd.entry_rect):
                self.mcd.draw_enter_message()
            elif self.stickman.rect.colliderect(self.hospital.entry_rect):
                self.hospital.draw_enter_message()
            elif self.stickman.rect.colliderect(self.office.entry_rect):
                self.office.draw_enter_message()
            elif self.stickman.rect.colliderect(self.castle.entry_rect):
                self.castle.draw_enter_message()
            elif self.stickman.rect.colliderect(self.drug_store.entry_rect):
                self.drug_store.draw_enter_message()
            elif self.stickman.rect.colliderect(self.weapon_shop.entry_rect):
                self.weapon_shop.draw_enter_message()
            elif self.stickman.rect.colliderect(self.bank.entry_rect):
                self.bank.draw_enter_message()

        elif self.home.entered:
            self.home.update()
        elif self.university.entered:
            self.university.update()
        elif self.mcd.entered:
            self.mcd.update()
        elif self.hospital.entered:
            self.hospital.update()
        elif self.office.entered:
            self.office.update()
        elif self.castle.entered:
            self.castle.update()
        elif self.drug_store.entered:
            self.drug_store.update()
        elif self.weapon_shop.entered:
            self.weapon_shop.update()
        elif self.bank.entered:
            self.bank.update()

        py.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
