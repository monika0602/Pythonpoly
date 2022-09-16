import pygame

from game import Board
from game.gameState import GameState
from game.round import Round


class Game:
    def __init__(self, game_mode):

        # Game state
        self.game_state = GameState(game_mode)

        # Graphics
        self.board = Board(self.game_state)

        # Round
        self.round = Round()

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_UP:
                    # Set dice
                    self.game_state.set_dice()
                    break
                elif event.key == pygame.K_DOWN:
                    # Delete dice
                    self.game_state.del_dice()
                    break
                elif event.key == pygame.K_1:
                    # Update text
                    self.game_state.update_text(add_text="trpspapa")
                    break
                elif event.key == pygame.K_2:
                    # Move pawn 0 to start
                    self.game_state.move_player_to_card(player_id=0, card_id=0)
                elif event.key == pygame.K_3:
                    # Move pawn 0 to start
                    self.round.id += 1
                    self.game_state.move_player_to_card(player_id=0, card_id=self.round.id + 30)
                    self.game_state.move_player_to_card(player_id=1, card_id=self.round.id + 30)
                    self.game_state.move_player_to_card(player_id=2, card_id=self.round.id + 30)
                    self.game_state.move_player_to_card(player_id=3, card_id=self.round.id + 30)
                    break

    def process_round(self):
        if self.round.id == 0:
            self.game_state.move_players_to_start()
        else:
            self.game_state.update_text(add_text="Remove")
            self.game_state.update_text(add_text=f"Runda: {self.round.id}")
            self.clock.tick(120)

    def run(self):
        while self.running:
            self.process_input()
            self.process_round()
            self.board.draw()
            self.clock.tick(60)
        print("Close game")

    def button_click(self, event):
        pass
