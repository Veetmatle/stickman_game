from buildings import Buildings
import pygame as py
import random
import time


class Castle(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(844, 197, 15, 42), image_path='Nerdy_Nade_castle.png')
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
            py.Rect(700, 750, 200, 50)  # Attack 3
        ]

        self.attack_text = None
        self.damage_text = None
        self.damage_pos = None
        self.damage_time = 0
        self.turn_text = None
        self.turn_text_time = 0

    def update_castle_image(self):
        if self.big_joe_defeated:
            self.image = py.image.load('3_en_unlocked_castle.png').convert()
        elif self.drunk_jimmy_defeated:
            self.image = py.image.load('3_en_unlocked_castle.png').convert()
        elif self.nerdy_nade_defeated:
            self.image = py.image.load('2_en_unlocked_castle.png').convert()
        else:
            self.image = py.image.load('Nerdy_Nade_castle.png').convert()

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.fight_nade_button.collidepoint(mouse_pos):
            self.message = "Click to fight Nade - lvl 8, str 40"
        elif self.fight_jimmy_button.collidepoint(mouse_pos) and self.nerdy_nade_defeated:
            self.message = "Click to fight Jimmy - lvl 16, str 80"
        elif self.fight_joe_button.collidepoint(mouse_pos) and self.nerdy_nade_defeated and self.drunk_jimmy_defeated:
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

    def handle_mouse_click(self, mouse_pos):
        if self.in_fight:
            if self.player_turn:
                self.handle_fight_click(mouse_pos)
        else:
            if self.fight_nade_button.collidepoint(mouse_pos):
                self.fight('Nade')
            elif self.fight_jimmy_button.collidepoint(mouse_pos) and self.nerdy_nade_defeated:
                self.fight('Jimmy')
            elif self.fight_joe_button.collidepoint(mouse_pos) and self.nerdy_nade_defeated and self.drunk_jimmy_defeated:
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

        if self.player_turn:
            self.turn_text = "Player's Turn"
        else:
            self.turn_text = f"{self.enemy}'s Turn"

        self.draw_text_with_outline(self.turn_text, (self.game.window_size[0] // 2, 100), (255, 255, 255), (0, 0, 0))

        mouse_pos = py.mouse.get_pos()
        for i, button in enumerate(self.attack_buttons):
            if self.player_turn and button.collidepoint(mouse_pos):
                py.draw.rect(self.game.screen, (0, 180, 0), button)  # Highlight button
            else:
                py.draw.rect(self.game.screen, (0, 128, 0), button)
            self.draw_text_with_outline(f'Attack {i + 1}', button.center, (255, 255, 255), (0, 0, 0))

        if self.attack_text:
            self.draw_text_with_outline(self.attack_text, (self.game.window_size[0] // 2, self.game.window_size[1] // 2), (255, 255, 255), (0, 0, 0))

        if self.damage_text and time.time() - self.damage_time < 1:
            self.draw_text_with_outline(self.damage_text, self.damage_pos, (255, 0, 0), (0, 0, 0))
        else:
            self.damage_text = None

        py.display.flip()

    def handle_fight_click(self, mouse_pos):
        for i, button in enumerate(self.attack_buttons):
            if button.collidepoint(mouse_pos):
                self.execute_attack(i)

    def execute_attack(self, attack_index):
        if attack_index == 0:
            damage = self.attack
            self.attack_text = "Player uses Attack 1"
            self.rage += 20
        elif attack_index == 1:
            damage = self.special_attack
            self.attack_text = "Player uses Special Attack"
            self.rage += 15
        elif attack_index == 2:
            damage = self.ultimate
            self.attack_text = "Player uses Ultimate Attack"
            self.rage += 30

        self.enemy_hp -= damage
        self.damage_text = f"-{damage}"
        self.damage_pos = (150, 80)
        self.damage_time = time.time()
        print(f"Dealt {damage} damage to {self.enemy}. Enemy HP is now {self.enemy_hp}")

        if self.enemy_hp <= 0:
            self.end_fight(victory=True)
        else:
            self.player_turn = False
            py.time.delay(1000)
            self.enemy_attack()

    def enemy_attack(self):
        if random.random() < 0.5:
            damage = self.enemy_ad
            self.attack_text = f"{self.enemy} uses Attack"
        else:
            damage = self.enemy_special_attack
            self.attack_text = f"{self.enemy} uses Special Attack"

        self.player_hp -= damage
        self.damage_text = f"-{damage}"
        self.damage_pos = (self.game.window_size[0] - 150, 80)
        self.damage_time = time.time()
        print(f"{self.enemy} dealt {damage} damage to Player. Player HP is now {self.player_hp}")

        if self.player_hp <= 0:
            self.end_fight(victory=False)
        else:
            self.player_turn = True
            py.time.delay(1000)

    def end_fight(self, victory):
        self.in_fight = False
        if victory:
            print(f"Player defeated {self.enemy}")
            if self.enemy == 'Nade':
                self.nerdy_nade_defeated = True
            elif self.enemy == 'Jimmy':
                self.drunk_jimmy_defeated = True
            elif self.enemy == 'Joe':
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
