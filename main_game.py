import sys
import pygame as py
from stickman_player import StickMan
from home_building import Home
from university_building import University
from MCdonalds import MCDonald
from hospital import Hospital
from office import Office

class Game:
    def __init__(self):
        py.init()
        self.window_size = (1000, 800)  # Rozmiar okna widocznego obszaru
        self.map_size = (2048, 1732)  # Rozmiar całej mapy
        self.screen = py.display.set_mode(self.window_size)
        py.display.set_caption('StickMan Jr')
        self.clock = py.time.Clock()
        self.running = True

        # Load background image
        self.background = py.image.load('game_background.png').convert()

        # Load collision mask
        collision_mask_image = py.image.load('maska.png').convert()
        self.collision_mask = py.mask.from_threshold(collision_mask_image, (255, 255, 255), (1, 1, 1, 255))

        # Init StickMan
        self.stickman = StickMan(self)

        # Init of buildings
        self.home = Home(self)
        self.university = University(self)
        self.mcd = MCDonald(self)
        self.hospital = Hospital(self)
        self.office = Office(self)


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limiting to 60 frames per second

        py.quit()
        sys.exit()

    def handle_events(self):
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

    def update(self):
        if not (self.home.entered or self.university.entered or self.mcd.entered or self.hospital.entered or self.office.entered):
            self.stickman.handle_keys()
        self.stickman.control_time_flow()
        self.hospital.check_conditions()

    def draw(self):
        if not (self.home.entered or self.university.entered or self.mcd.entered or self.hospital.entered or self.office.entered):
            # Ustal pozycję kamery
            camera_x = max(0, min(self.stickman.rect.centerx - self.window_size[0] // 2, self.map_size[0] - self.window_size[0]))
            camera_y = max(0, min(self.stickman.rect.centery - self.window_size[1] // 2, self.map_size[1] - self.window_size[1]))
            camera_offset = (-camera_x, -camera_y)

            # Rysuj tło z przesunięciem kamery
            self.screen.blit(self.background, camera_offset)
            self.stickman.draw(self.screen, camera_offset)

            # Rysuj pasek doświadczenia, poziom, hp
            self.stickman.draw_properties()

            # Sprawdź, czy gracz jest w pobliżu wejścia do domku
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

        py.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
