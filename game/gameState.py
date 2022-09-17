from pygame import Vector2

import constants
from cards import cardsList
from game import Dice
from game.Player import Player
from chances import chancesList


class GameState:
    def __init__(self, game_mode):
        self.dice = None
        self.ai_players_count = game_mode
        self.players = self.set_players()
        self.cards = cardsList.get_cards_from_csv()
        self.chancesList = chancesList.get_chances_from_csv()
        self.text = constants.TEXT_START
        self.round_id = 0
        self.current_player_id = -1
        print(f'Run game with mode {self.ai_players_count}')

    def set_dice(self):
        self.dice = Dice()

    def del_dice(self):
        self.dice = None

    # Creates list of players
    def set_players(self):
        list_of_players = [Player(0, "human")]

        for x in range(1, self.ai_players_count + 1):
            list_of_players.append(Player(x, "AI"))

        return list_of_players

    def turn_off_player(self, player_id):
        self.players[player_id].set_status()

    def set_card_owner(self, card_id, player_id):
        self.cards[card_id].owner = player_id

    def del_card_owner(self, card_id):
        self.cards[card_id].owner = None
        self.cards[card_id].buildings = None

    def update_text(self, add_text="Remove"):
        if add_text == "Remove":
            self.text = ""
        else:
            self.text = "{} {}".format(self.text, add_text)

    def move_player_to_card(self, player_id, card_id):
        card_position = Vector2(self.cards[card_id].position_h, self.cards[card_id].position_w)
        self.players[player_id].move_pawn(card_position, card_id)

    def move_players_to_start(self):
        for player in self.players:
            self.move_player_to_card(player.player_id, 0)

    def end_round(self):
        self.current_player_id = self.set_next_player()
        self.round_id += 1
        self.update_text(add_text="Remove")
        self.update_text(add_text=f" Tura {self.round_id} \n")
        self.update_text(add_text=f" Gracz nr {self.current_player_id + 1} \n")

    def set_next_player(self):
        new_id = self.current_player_id
        while True:
            new_id += 1
            if new_id > self.ai_players_count:
                new_id = -1
            elif self.players[new_id].status == 1:
                break

        return new_id

    def process_card_event(self):
        player_id = self.current_player_id
        card_id = self.players[player_id].current_card
        card_type = self.cards[card_id].class_type
        if card_type == "ActionCard":
            # event for action cards
            self.update_text(add_text=f"Jesteś na karcie specjalnej.\n")
            if self.cards[card_id].card_type == "Chance":
                self.update_text(add_text=f"Losowanie karty z szansa...\n")
                # event for chance
        elif card_type == "Street":
            self.update_text(add_text=f"Jesteś na karcie biblioteki.\n")
            self.check_ownership(card_id)
        elif card_type == "Company":
            self.update_text(add_text=f"Jesteś na karcie firmy.\n")
            self.check_ownership(card_id)


    def check_ownership(self, card_id):

        if self.cards[card_id].owner is None:
            self.update_text(add_text=f"Karta jest dostępna do zakupu.\n")
            # buy_card() - there are two types of cards : street and company
        elif self.cards[card_id].owner != self.current_player_id:
            self.update_text(add_text=f"Musisz zapłacić graczowi.\n")
            # pay_to(owner)  - there are two types of cards : street and company
        else:
            self.update_text(add_text=f"Karta należy do ciebie.\n")
