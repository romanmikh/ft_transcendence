from ..utils.settings import *
from .sprites import *
import time
import json

class Game:
    def __init__(self):
        self.scores = {"player1": 0, "player2": 0}
        self.running = True

        # make pad & ball sprites
        pad_left  = PlayerPad(POS['padl_start'], "player1", None, self.all_sprites)
        # pad_right = PlayerPad(POS['padr_start'], "player2", None, self.all_sprites)
        # pad_right = DumbOpponentPad(POS['padr_start'], "DumbBot", None, self.all_sprites)
        # pad_right = FollowOpponentPad(POS['padr_start'], "KeenBot", None, self.all_sprites)
        pad_right = SmartOpponentPad(POS['padr_start'], "SmartBot", None, self.all_sprites)
        self.ball = Ball(POS['ball_start'], (pad_left, pad_right), self.scores, self.all_sprites)

    def run(self):
        while self.running:

            # event loop
            delta_time = self.clock.tick() / 1000  # for framerate independence
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    with open(SCORE_FILE_PATH, 'w') as f:
                        json.dump(self.scores, f)

            # handle game state
            if not self.ball.game_active_ever:
                # display_instructions()
            elif self._check_win():
                # self._handle_win()
            else:
                # display_score()
            
            # send state to client

        # pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()