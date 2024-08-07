import pygame as py
import random
import time
from buildings import Buildings

class Castle(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(844, 197, 15, 42), image_path='images/Nerdy_Nade_castle.png')
        self.nerdy_nade_defeated = False
        self.drunk_jimmy_defeated = False
        self.big_joe_defeated = False
        self.update_castle_image()

        self.fight_nade_button = py.Rect(118, 393, 230, 296)
        self.fight_jimmy_button = py.Rect(642, 382, 264, 308)
        self.fight_joe_button = py.Rect(408, 262, 184, 300)
        self.in_fight = False
        self.enemy = None

        # player stats
        self.player_hp = 1000
        self.attack = 150
        self.special_attack = 400
        self.ultimate = 700
        self.rage = 0
        self.energy = 100
        self.player_turn = True

        # enemy stats
        self.nade_stats = {'hp': 800, 'ad': 100, 'special_attack': 200}
        self.jimmy_stats = {'hp': 1500, 'ad': 200, 'special_attack': 400}
        self.joe_stats = {'hp': 2500, 'ad': 300, 'special_attack': 600}

        # attack buttons
        self.attack_buttons = [
            py.Rect(100, 750, 200, 50),  # Attack 1
            py.Rect(400, 750, 200, 50),  # Attack 2
            py.Rect(700, 750, 200, 50)   # Attack 3
        ]

        self.damage_texts = []

    def update_castle_image(self):
        if self.big_joe_defeated:
            self.image = py.image.load('images/3_en_unlocked_castle.png').convert()
        elif self.drunk_jimmy_defeated:
            self.image = py.image.load('images/3_en_unlocked_castle.png').convert()
        elif self.nerdy_nade_defeated:
            self.image = py.image.load('images/2_en_unlocked_castle.png').convert()
        else:
            self.image = py.image.load('images/Nerdy_Nade_castle.png').convert()

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.fight_nade_button.collidepoint(mouse_pos) and not self.nerdy_nade_defeated:
            self.message = "Click to fight Nade - lvl 8, str 40"
        elif self.fight_jimmy_button.collidepoint(mouse_pos) and self.nerdy_nade_defeated and not self.drunk_jimmy_defeated:
            self.message = "Click to fight Jimmy - lvl 16, str 80"
        elif self.fight_joe_button.collidepoint(mouse_pos) and self.nerdy_nade_defeated and self.drunk_jimmy_defeated and not self.big_joe_defeated:
            self.message = "Click to fight Joe - lvl 25, str 120."
        else:
            self.message = "Click esc to exit"

        if self.message != previous_message:
            self.draw_message()

    def draw_message(self):
        image_scaled = py.transform.scale(self.image, self.game.window_size)
        self.game.screen.blit(image_scaled, (0, 0))
        if self.message:
            self.draw_text_with_outline(self.message, (self.game.window_size[0] // 2, self.game.window_size[1] - 30), (255, 0, 0), (0, 0, 0))
        py.display.flip()

    def update(self):
        if self.entered:
            if self.in_fight:
                self.draw_fight()
            else:
                self.handle_buttons()
                self.draw_message()
        self.update_damage_texts()

    def draw_text_with_outline(self, text, pos, color, outline_color, background_color=None):
        font = py.font.SysFont(None, 30)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)

        if background_color:
            background_rect = text_rect.inflate(20, 10)
            py.draw.rect(self.game.screen, background_color, background_rect, border_radius=5)
            py.draw.rect(self.game.screen, outline_color, background_rect, 2, border_radius=5)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            outline_surf = font.render(text, True, outline_color)
            outline_rect = outline_surf.get_rect(center=(text_rect.centerx + dx, text_rect.centery + dy))
            self.game.screen.blit(outline_surf, outline_rect)

        self.game.screen.blit(text_surf, text_rect)

    def update_damage_texts(self):
        current_time = time.time()
        new_damage_texts = []
        for text, pos, creation_time in self.damage_texts:
            elapsed = current_time - creation_time
            if elapsed < 2.0:
                alpha = max(0, 255 - int((elapsed / 2.0) * 255))
                self.draw_damage_text(text, pos, alpha)
                new_damage_texts.append((text, pos, creation_time))
        self.damage_texts = new_damage_texts

    def draw_damage_text(self, text, pos, alpha):
        font = py.font.SysFont(None, 30)
        text_surf = font.render(text, True, (255, 0, 0))
        text_surf.set_alpha(alpha)
        text_rect = text_surf.get_rect(center=pos)

        background_rect = text_rect.inflate(20, 10)
        py.draw.rect(self.game.screen, (255, 255, 255), background_rect, border_radius=5)
        py.draw.rect(self.game.screen, (0, 0, 0), background_rect, 2, border_radius=5)

        self.game.screen.blit(text_surf, text_rect)

    def handle_mouse_click(self, mouse_pos):
        if self.in_fight:
            if self.player_turn:
                self.handle_fight_click(mouse_pos)
        else:
            if self.fight_nade_button.collidepoint(mouse_pos) and not self.nerdy_nade_defeated:
                self.fight('Nade')
            elif self.fight_jimmy_button.collidepoint(mouse_pos) and self.nerdy_nade_defeated and not self.drunk_jimmy_defeated:
                self.fight('Jimmy')
            elif self.fight_joe_button.collidepoint(mouse_pos) and self.nerdy_nade_defeated and self.drunk_jimmy_defeated and not self.big_joe_defeated:
                self.fight('Joe')

    def fight(self, enemy):
        self.in_fight = True
        self.enemy = enemy
        if enemy == 'Nade':
            self.enemy_hp = self.nade_stats['hp']
            self.enemy_ad = self.nade_stats['ad']
            self.enemy_special_attack = self.nade_stats['special_attack']
            self.image = py.image.load('fight_nade.jpg').convert()
        elif enemy == 'Jimmy':
            self.enemy_hp = self.jimmy_stats['hp']
            self.enemy_ad = self.jimmy_stats['ad']
            self.enemy_special_attack = self.jimmy_stats['special_attack']
            self.image = py.image.load('fight_jimmy.jpg').convert()
        elif enemy == 'Joe':
            self.enemy_hp = self.joe_stats['hp']
            self.enemy_ad = self.joe_stats['ad']
            self.enemy_special_attack = self.joe_stats['special_attack']
            self.image = py.image.load('fight_joe.jpg').convert()
        print(f"Started fight with {self.enemy}")

    def draw_fight(self):
        image_scaled = py.transform.scale(self.image, self.game.window_size)
        self.game.screen.blit(image_scaled, (0, 0))

        self.draw_text_with_outline(f'Player HP: {self.player_hp}', (self.game.window_size[0] - 150, 50), (255, 0, 0), (0, 0, 0), (255, 255, 255))
        self.draw_text_with_outline(f'Rage: {self.rage}', (self.game.window_size[0] - 150, 100), (255, 0, 0), (0, 0, 0), (255, 255, 255))
        self.draw_text_with_outline(f'{self.enemy} HP: {self.enemy_hp}', (150, 50), (255, 0, 0), (0, 0, 0), (255, 255, 255))

        mouse_pos = py.mouse.get_pos()
        attack_names = ['Normal Attack', 'Special Attack', 'Ultimate Attack']

        for i, button in enumerate(self.attack_buttons):
            if self.player_turn and button.collidepoint(mouse_pos):
                py.draw.rect(self.game.screen, (128, 128, 128), button)
            else:
                py.draw.rect(self.game.screen, (0, 0, 0), button)
            self.draw_text_with_outline(attack_names[i], button.center, (255, 255, 255), (0, 0, 0))

        py.display.flip()

    def handle_fight_click(self, mouse_pos):
        for i, button in enumerate(self.attack_buttons):
            if button.collidepoint(mouse_pos):
                self.execute_attack(i)

    def execute_attack(self, attack_index):
        if attack_index == 0:
            damage = self.attack
            self.attack_text = "Player uses Normal Attack"
            self.rage += 20
        elif attack_index == 1 and self.rage >= 20:
            damage = self.special_attack
            self.attack_text = "Player uses Special Attack"
            self.rage -= 20
        elif attack_index == 2 and self.rage >= 60:
            damage = self.ultimate
            self.attack_text = "Player uses Ultimate Attack"
            self.rage -= 60
        else:
            return  # Nie wykonuj ataku, jeśli nie ma wystarczająco dużo rage

        self.enemy_hp -= damage
        self.add_damage_text(f"-{damage}", (self.game.window_size[0] // 2 - 150, 50))
        print(f"Dealt {damage} damage to {self.enemy}. Enemy HP is now {self.enemy_hp}")

        py.display.flip()

        if self.enemy_hp <= 0:
            self.end_fight(victory=True)
        else:
            self.player_turn = False
            py.time.delay(1000)
            self.enemy_attack()

    def add_damage_text(self, text, pos):
        self.damage_texts.append((text, pos, time.time()))

    def enemy_attack(self):
        if random.random() < 0.5:
            damage = self.enemy_ad
            self.attack_text = f"{self.enemy} uses Attack"
        else:
            damage = self.enemy_special_attack
            self.attack_text = f"{self.enemy} uses Special Attack"

        self.player_hp -= damage
        self.add_damage_text(f"-{damage}", (self.game.window_size[0] - 150, 150))
        print(f"{self.enemy} dealt {damage} damage to Player. Player HP is now {self.player_hp}")

        py.display.flip()

        if self.player_hp <= 0:
            self.end_fight(victory=False)
        else:
            self.player_turn = True
            py.time.delay(1000)

    def end_fight(self, victory):
        self.in_fight = False
        if victory:
            self.game.stickman.level += 5
            print(f"Player defeated {self.enemy}")
            if self.enemy == 'Nade':
                self.game.stickman.money += 100
                self.nerdy_nade_defeated = True
            elif self.enemy == 'Jimmy':
                self.game.stickman.money += 200
                self.drunk_jimmy_defeated = True
            elif self.enemy == 'Joe':
                self.game.stickman.money += 500
                self.big_joe_defeated = True
        else:
            print("Player was defeated")

        self.update_castle_image()
        self.enemy = None
        self.game.stickman.draw_properties()
        self.reset_stats()
        py.display.flip()

    def reset_stats(self):
        self.player_hp = 1000
        self.attack = 150
        self.special_attack = 400
        self.ultimate = 700
        self.rage = 0
        self.energy = 100
        self.player_turn = True
        self.game.stickman.tiredness = 90
        self.game.stickman.hunger = 90
