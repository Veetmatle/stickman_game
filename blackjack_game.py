import pygame as py
import random
import copy
import sys
import time


class BlackjackGame:
    def __init__(self, window_size):
        self.window_size = window_size

        # Load card images
        self.icon = py.image.load('resources/icon.png')
        self.cBack = py.image.load('resources/cards/cardback.png')
        self.diamondA = py.image.load('resources/cards/ad.png')
        self.clubA = py.image.load('resources/cards/ac.png')
        self.heartA = py.image.load('resources/cards/ah.png')
        self.spadeA = py.image.load('resources/cards/as.png')
        self.diamond2 = py.image.load('resources/cards/2d.png')
        self.club2 = py.image.load('resources/cards/2c.png')
        self.heart2 = py.image.load('resources/cards/2h.png')
        self.spade2 = py.image.load('resources/cards/2s.png')
        self.diamond3 = py.image.load('resources/cards/3d.png')
        self.club3 = py.image.load('resources/cards/3c.png')
        self.heart3 = py.image.load('resources/cards/3h.png')
        self.spade3 = py.image.load('resources/cards/3s.png')
        self.diamond4 = py.image.load('resources/cards/4d.png')
        self.club4 = py.image.load('resources/cards/4c.png')
        self.heart4 = py.image.load('resources/cards/4h.png')
        self.spade4 = py.image.load('resources/cards/4s.png')
        self.diamond5 = py.image.load('resources/cards/5d.png')
        self.club5 = py.image.load('resources/cards/5c.png')
        self.heart5 = py.image.load('resources/cards/5h.png')
        self.spade5 = py.image.load('resources/cards/5s.png')
        self.diamond6 = py.image.load('resources/cards/6d.png')
        self.club6 = py.image.load('resources/cards/6c.png')
        self.heart6 = py.image.load('resources/cards/6h.png')
        self.spade6 = py.image.load('resources/cards/6s.png')
        self.diamond7 = py.image.load('resources/cards/7d.png')
        self.club7 = py.image.load('resources/cards/7c.png')
        self.heart7 = py.image.load('resources/cards/7h.png')
        self.spade7 = py.image.load('resources/cards/7s.png')
        self.diamond8 = py.image.load('resources/cards/8d.png')
        self.club8 = py.image.load('resources/cards/8c.png')
        self.heart8 = py.image.load('resources/cards/8h.png')
        self.spade8 = py.image.load('resources/cards/8s.png')
        self.diamond9 = py.image.load('resources/cards/9d.png')
        self.club9 = py.image.load('resources/cards/9c.png')
        self.heart9 = py.image.load('resources/cards/9h.png')
        self.spade9 = py.image.load('resources/cards/9s.png')
        self.diamond10 = py.image.load('resources/cards/10d.png')
        self.club10 = py.image.load('resources/cards/10c.png')
        self.heart10 = py.image.load('resources/cards/10h.png')
        self.spade10 = py.image.load('resources/cards/10s.png')
        self.diamondJ = py.image.load('resources/cards/jd.png')
        self.clubJ = py.image.load('resources/cards/jc.png')
        self.heartJ = py.image.load('resources/cards/jh.png')
        self.spadeJ = py.image.load('resources/cards/js.png')
        self.diamondQ = py.image.load('resources/cards/qd.png')
        self.clubQ = py.image.load('resources/cards/qc.png')
        self.heartQ = py.image.load('resources/cards/qh.png')
        self.spadeQ = py.image.load('resources/cards/qs.png')
        self.diamondK = py.image.load('resources/cards/kd.png')
        self.clubK = py.image.load('resources/cards/kc.png')
        self.heartK = py.image.load('resources/cards/kh.png')
        self.spadeK = py.image.load('resources/cards/ks.png')

        # Set icon
        py.display.set_icon(self.icon)

        # Colors and background settings
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (192, 192, 192)
        self.background_color = (20, 140, 40)

        # Card lists
        self.cards = [self.diamondA, self.clubA, self.heartA, self.spadeA,
                      self.diamond2, self.club2, self.heart2, self.spade2,
                      self.diamond3, self.club3, self.heart3, self.spade3,
                      self.diamond4, self.club4, self.heart4, self.spade4,
                      self.diamond5, self.club5, self.heart5, self.spade5,
                      self.diamond6, self.club6, self.heart6, self.spade6,
                      self.diamond7, self.club7, self.heart7, self.spade7,
                      self.diamond8, self.club8, self.heart8, self.spade8,
                      self.diamond9, self.club9, self.heart9, self.spade9,
                      self.diamond10, self.club10, self.heart10, self.spade10,
                      self.diamondJ, self.clubJ, self.heartJ, self.spadeJ,
                      self.diamondQ, self.clubQ, self.heartQ, self.spadeQ,
                      self.diamondK, self.clubK, self.heartK, self.spadeK]

        self.cardA = [self.diamondA, self.clubA, self.heartA, self.spadeA]
        self.card2 = [self.diamond2, self.club2, self.heart2, self.spade2]
        self.card3 = [self.diamond3, self.club3, self.heart3, self.spade3]
        self.card4 = [self.diamond4, self.club4, self.heart4, self.spade4]
        self.card5 = [self.diamond5, self.club5, self.heart5, self.spade5]
        self.card6 = [self.diamond6, self.club6, self.heart6, self.spade6]
        self.card7 = [self.diamond7, self.club7, self.heart7, self.spade7]
        self.card8 = [self.diamond8, self.club8, self.heart8, self.spade8]
        self.card9 = [self.diamond9, self.club9, self.heart9, self.spade9]
        self.card10 = [self.diamond10, self.club10, self.heart10, self.spade10,
                       self.diamondJ, self.clubJ, self.heartJ, self.spadeJ,
                       self.diamondQ, self.clubQ, self.heartQ, self.spadeQ,
                       self.diamondK, self.clubK, self.heartK, self.spadeK]

    def get_amt(self, card):
        """Returns the value of a card."""
        if card in self.cardA:
            return 11
        elif card in self.card2:
            return 2
        elif card in self.card3:
            return 3
        elif card in self.card4:
            return 4
        elif card in self.card5:
            return 5
        elif card in self.card6:
            return 6
        elif card in self.card7:
            return 7
        elif card in self.card8:
            return 8
        elif card in self.card9:
            return 9
        elif card in self.card10:
            return 10
        else:
            print('get_amt error')
            exit()

    def gen_card(self, c_list, x_list):
        """
        Generates a card from c_list, removes it from c_list, and adds it to x_list.
        Returns whether the card is an Ace and the card itself.
        """
        card = random.choice(c_list)
        c_list.remove(card)
        x_list.append(card)
        return card, (1 if card in self.cardA else 0)

    def init_game(self, c_list, u_list, d_list):
        """
        Generates two cards each for the dealer and the player, alternating between them.
        Returns whether each card is an Ace and the total value of cards for each person.
        """
        userA, dealA = 0, 0
        card1, cA = self.gen_card(c_list, u_list)
        userA += cA
        card2, cA = self.gen_card(c_list, d_list)
        dealA += cA
        card3, cA = self.gen_card(c_list, u_list)
        userA += cA
        card4, cA = self.gen_card(c_list, d_list)
        dealA += cA
        return self.get_amt(card1) + self.get_amt(card3), userA, self.get_amt(card2) + self.get_amt(card4), dealA

    def display_points(self, screen, font, user_sum, deal_sum, deal_cards):
        """Displays the current points of the player and the dealer."""
        user_points_text = font.render(f'Your points: {user_sum}', True, self.black)
        dealer_points_text = font.render(f'Dealer points: {deal_sum}', True, self.black)

        screen.blit(user_points_text, (10, self.window_size[1] - 120))

        if deal_cards:
            dealer_x_position = 10 + len(deal_cards) * 110 + 20
            screen.blit(dealer_points_text, (dealer_x_position, 30))

    def display_end_message(self, screen, result):
        """Displays the end-of-game message."""
        message = "You won!" if result == 'win' else "You lost!"
        font = py.font.SysFont('arial', 48, bold=True)
        end_text = font.render(message, True, self.white)

        text_rect = end_text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2))
        screen.blit(end_text, text_rect)
        py.display.flip()
        time.sleep(2)

    def play(self, stake, stickman):
        """Plays a round of Blackjack."""
        ccards = copy.copy(self.cards)
        stand = False
        user_card = []
        deal_card = []

        py.init()
        screen = py.display.set_mode(self.window_size)
        py.display.set_caption('Blackjack')
        font = py.font.SysFont('arial', 28, bold=True)
        hit_txt = font.render('Hit', 1, self.black)
        stand_txt = font.render('Stand', 1, self.black)
        user_sum, userA, deal_sum, dealA = self.init_game(ccards, user_card, deal_card)

        background = py.Surface(screen.get_size())
        background = background.convert()
        background.fill(self.background_color)
        hitB = py.draw.rect(background, self.gray, (10, self.window_size[1] - 55, 75, 35))
        standB = py.draw.rect(background, self.gray, (95, self.window_size[1] - 55, 75, 35))

        gameover = False

        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    return 'quit'
                elif event.type == py.MOUSEBUTTONDOWN and not gameover:
                    if hitB.collidepoint(event.pos):
                        card, cA = self.gen_card(ccards, user_card)
                        userA += cA
                        user_sum += self.get_amt(card)
                        if user_sum > 21 and userA > 0:
                            user_sum -= 10
                            userA -= 1
                    elif standB.collidepoint(event.pos):
                        stand = True
                        while deal_sum < 17:
                            card, cA = self.gen_card(ccards, deal_card)
                            dealA += cA
                            deal_sum += self.get_amt(card)
                            if deal_sum > 21 and dealA > 0:
                                deal_sum -= 10
                                dealA -= 1
                        gameover = True

            if user_sum > 21:
                screen.blit(background, (0, 0))
                self.display_points(screen, font, user_sum, deal_sum, deal_card)
                for card in deal_card:
                    x = 10 + deal_card.index(card) * 110
                    screen.blit(card, (x, 10))
                py.display.update()
                self.display_end_message(screen, 'lose')
                return 'lose'
            elif stand:
                screen.blit(background, (0, 0))
                self.display_points(screen, font, user_sum, deal_sum, deal_card)
                for card in deal_card:
                    x = 10 + deal_card.index(card) * 110
                    screen.blit(card, (x, 10))
                py.display.update()
                if deal_sum > 21 or user_sum > deal_sum:
                    self.display_end_message(screen, 'win')
                    return 'win'
                else:
                    self.display_end_message(screen, 'lose')
                    return 'lose'

            screen.blit(background, (0, 0))
            screen.blit(hit_txt, (39, self.window_size[1] - 50))
            screen.blit(stand_txt, (116, self.window_size[1] - 50))

            for card in user_card:
                x = 10 + user_card.index(card) * 110
                screen.blit(card, (x, 295))

            if not stand and not gameover:
                screen.blit(self.cBack, (120, 10))

            self.display_points(screen, font, user_sum, deal_sum, deal_card)

            py.display.update()

    def prompt_for_stake(self, max_stake):
        """
        Prompts the player to enter a stake amount.
        Shows the maximum possible stake.
        Returns the stake amount entered by the player or None if invalid.
        """
        py.init()
        font = py.font.SysFont('arial', 32, bold=True)
        input_box = py.Rect(300, 300, 200, 50)
        color_inactive = py.Color('lightskyblue3')
        color_active = py.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        screen = py.display.set_mode(self.window_size)
        py.display.set_caption('Enter your stake')

        while not done:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == py.KEYDOWN:
                    if active:
                        if event.key == py.K_RETURN:
                            if text.isdigit() and 0 < int(text) <= max_stake:
                                return int(text)
                            else:
                                return None
                        elif event.key == py.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill((30, 30, 30))
            prompt_text = font.render(f"Enter your stake (max: {max_stake}):", True, py.Color('white'))
            screen.blit(prompt_text, (250, 250))

            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            py.draw.rect(screen, color, input_box, 2)

            py.display.flip()
