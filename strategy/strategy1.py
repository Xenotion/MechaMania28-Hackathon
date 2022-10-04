from abc import abstractmethod
from game.game_state import GameState
from game.item import Item
import game.character_class

from game.position import Position
from random import Random
from util.utility import chebyshev_distance
from game.position import Position
from strategy.strategy import Strategy

class Strategy1(Strategy):
    
    direction = 0
    spawn_point = 0
    player_list = [0, 1, 2, 3]


    def at_spawn(self, game_state: GameState, my_player_index: int) -> bool:
        if game_state.player_state_list[my_player_index].position.x == 0 and game_state.player_state_list[my_player_index].position.y == 0:
            self.spawn_point = 0
            return True
        elif game_state.player_state_list[my_player_index].position.x == 0 and game_state.player_state_list[my_player_index].position.y == 9:
            self.spawn_point = 1
            return True
        elif game_state.player_state_list[my_player_index].position.x == 9 and game_state.player_state_list[my_player_index].position.y == 0:
            self.spawn_point = 2
            return True
        elif game_state.player_state_list[my_player_index].position.x == 9 and game_state.player_state_list[my_player_index].position.y == 9:
            self.spawn_point = 3
            return True
        else:
            return False

    def at_cap(self, game_state: GameState, my_player_index: int) -> bool:
        if game_state.player_state_list[my_player_index].position.x == 4 and game_state.player_state_list[my_player_index].position.y == 4:
            return True
        elif game_state.player_state_list[my_player_index].position.x == 4 and game_state.player_state_list[my_player_index].position.y == 5:
            return True
        elif game_state.player_state_list[my_player_index].position.x == 5 and game_state.player_state_list[my_player_index].position.y == 4:
            return True
        elif game_state.player_state_list[my_player_index].position.x == 5 and game_state.player_state_list[my_player_index].position.y == 5:
            return True
        else:
            return False

    """Before the game starts, pick a class for your bot to start with.
    :returns: A game.CharacterClass Enum.
    """
    
    def strategy_initialize(self, my_player_index: int) -> None:
        return game.character_class.CharacterClass.KNIGHT

    """Each turn, decide if you should use the item you're holding. Do not try to use the
    legendary Item.None!
    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.
    :returns: If you want to use your item
    """
    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        if game_state.player_state_list[my_player_index].position.x == 0 and game_state.player_state_list[my_player_index].position.y == 0:
            self.spawn_point = 0
        elif game_state.player_state_list[my_player_index].position.x == 9 and game_state.player_state_list[my_player_index].position.y == 0:
            self.spawn_point = 1
        elif game_state.player_state_list[my_player_index].position.x == 0 and game_state.player_state_list[my_player_index].position.y == 9:
            self.spawn_point = 2
        elif game_state.player_state_list[my_player_index].position.x == 9 and game_state.player_state_list[my_player_index].position.y == 9:
            self.spawn_point = 3
        return False

    
    """Each turn, pick a position on the board that you want to move towards. Be careful not to
    fall out of the board!
    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.
    :returns: A game.Position object.
    """
    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        if (not self.at_cap(game_state, my_player_index)):
            if self.spawn_point == 0:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 1:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 2:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y - 1)
                return destination

            elif self.spawn_point == 3:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y - 1)
                return destination
        else:
            return game_state.player_state_list[my_player_index].position

    """Each turn, pick a player you would like to attack. Feel free to be a pacifist and attack no
    one but yourself.
    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.
    :returns: Your target's player index.
    """
    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        if my_player_index in self.player_list:
            self.player_list.pop(my_player_index)
        min_health = 9
        min_health_enemy = -1
        for i in range(len(self.player_list)):
            if chebyshev_distance(game_state.player_state_list[my_player_index].position, game_state.player_state_list[self.player_list[i]].position) <= 1:
                if game_state.player_state_list[self.player_list[i]].health <= min_health:
                    min_health_enemy = self.player_list[i]
                    min_health = game_state.player_state_list[self.player_list[i]].health

        if min_health_enemy == -1:
            return self.player_list[0]
        else:
            return min_health_enemy
            
    """Each turn, pick an item you want to buy. Return Item.None if you don't think you can
    afford anything.
    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.
    :returns: A game.Item object.
    """
    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        return Item.NONE
        # if self.use_action_decision(game_state, my_player_index) and (game_state.player_state_list[my_player_index].item == Item.NONE.name) and (game_state.player_state_list[my_player_index].gold >= 5):
        #     return Item.SPEED_POTION