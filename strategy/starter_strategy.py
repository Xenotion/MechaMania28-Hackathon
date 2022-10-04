from abc import abstractmethod
from game.game_state import GameState
from game.item import Item
import game.character_class

from game.position import Position
from random import Random
from util.utility import chebyshev_distance
from strategy.strategy import Strategy

class StarterStrategy(Strategy):

    spawn_point = 0
    player_list = [0, 1, 2, 3]
    movement_status = 1
    spawn_duration = 0

    def archer_count(self, game_state: GameState, my_player_index: int) -> bool:
        archer_count = 0
        for i in range(len(self.player_list)):
            if game_state.player_state_list[self.player_list[i]].character_class == game.character_class.CharacterClass.ARCHER:
                archer_count += 1
        return archer_count >= 2


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

    def predict_movement(self, game_state: GameState, my_player_index: int) -> Position:
        if self.at_spawn(game_state, my_player_index) and self.spawn_duration == 0:
            if game_state.player_state_list[my_player_index].gold >= 4:
                return game_state.player_state_list[my_player_index].position

        if self.movement_status == 1:
            if self.spawn_point == 0:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 2, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 1:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 2, game_state.player_state_list[my_player_index].position.y - 1)
                return destination

            elif self.spawn_point == 2:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 2, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 3:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 2, game_state.player_state_list[my_player_index].position.y - 1)
                return destination

        elif (self.movement_status == 2):
            if self.spawn_point == 0:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y + 2)
                return destination

            elif self.spawn_point == 1:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y - 2)
                return destination

            elif self.spawn_point == 2:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y + 2)
                return destination

            elif self.spawn_point == 3:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y - 2)
                return destination

        elif (self.movement_status == 3):
            if self.spawn_point == 0:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 1:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y - 1)
                return destination

            elif self.spawn_point == 2:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 3:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y - 1)
                return destination
        elif (self.movement_status == 4):
            return game_state.player_state_list[my_player_index].position


    """Before the game starts, pick a class for your bot to start with.
    :returns: A game.CharacterClass Enum.
    """
    def strategy_initialize(self, my_player_index: int) -> None:
        return game.character_class.CharacterClass.ARCHER

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
        elif game_state.player_state_list[my_player_index].position.x == 9 and game_state.player_state_list[my_player_index].position.y == 9:
            self.spawn_point = 2
        elif game_state.player_state_list[my_player_index].position.x == 0 and game_state.player_state_list[my_player_index].position.y == 9:
            self.spawn_point = 3

        # destination = self.predict_movement(game_state, my_player_index)

        # if my_player_index in self.player_list:
        #     self.player_list.pop(my_player_index)
        # min_health = 9
        # min_health_enemy = -1
        # for i in range(len(self.player_list)):
        #     if chebyshev_distance(destination, game_state.player_state_list[self.player_list[i]].position) <= 4:
        #         if game_state.player_state_list[self.player_list[i]].health <= min_health:
        #             min_health_enemy = self.player_list[i]
        #             min_health = game_state.player_state_list[self.player_list[i]].health
                    
        
        return self.movement_status == 3

    
    """Each turn, pick a position on the board that you want to move towards. Be careful not to
    fall out of the board!
    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.
    :returns: A game.Position object.
    """
    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        if self.archer_count(game_state, my_player_index):
            if self.at_spawn(game_state, my_player_index) and self.spawn_duration == 0:
                if game_state.player_state_list[my_player_index].gold >= 7:
                    self.spawn_duration = 1
                    self.movement_status = 1
                    return game_state.player_state_list[my_player_index].position
                else:
                    self.movement_status = 1
        else:
            if self.at_spawn(game_state, my_player_index) and self.spawn_duration == 0:
                if game_state.player_state_list[my_player_index].gold >= 4:
                    self.spawn_duration = 1
                    self.movement_status = 1
                    return game_state.player_state_list[my_player_index].position
                else:
                    self.movement_status = 1
            

        if self.movement_status == 1:
            self.movement_status = 2
            if self.spawn_point == 0:
                self.spawn_duration = 0
                destination = Position(game_state.player_state_list[my_player_index].position.x + 2, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 1:
                self.spawn_duration = 0
                destination = Position(game_state.player_state_list[my_player_index].position.x + 2, game_state.player_state_list[my_player_index].position.y - 1)
                return destination

            elif self.spawn_point == 2:
                self.spawn_duration = 0
                destination = Position(game_state.player_state_list[my_player_index].position.x - 2, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 3:
                self.spawn_duration = 0
                destination = Position(game_state.player_state_list[my_player_index].position.x - 2, game_state.player_state_list[my_player_index].position.y - 1)
                return destination

        elif (self.movement_status == 2):
            self.movement_status = 3
            if self.spawn_point == 0:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y + 2)
                return destination

            elif self.spawn_point == 1:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y - 2)
                return destination

            elif self.spawn_point == 2:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y + 2)
                return destination

            elif self.spawn_point == 3:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y - 2)
                return destination
        elif (self.movement_status == 3):
            self.movement_status = 4
            if self.spawn_point == 0:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 1:
                destination = Position(game_state.player_state_list[my_player_index].position.x + 1, game_state.player_state_list[my_player_index].position.y - 1)
                return destination

            elif self.spawn_point == 2:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y + 1)
                return destination

            elif self.spawn_point == 3:
                destination = Position(game_state.player_state_list[my_player_index].position.x - 1, game_state.player_state_list[my_player_index].position.y - 1)
                return destination
        elif (self.movement_status == 4):
            return game_state.player_state_list[my_player_index].position

    """Each turn, pick a player you would like to attack. Feel free to be a pacifist and attack no
    one but yourself.
    :param gameState:     A provided GameState object, contains every piece of info on the game board.
    :param myPlayerIndex: You may find out which player on the board you are.
    :returns: Your target's player index.
    """
    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        if self.movement_status == 3:
            if my_player_index in self.player_list:
                self.player_list.pop(my_player_index)
            max_health = 0
            max_health_enemy = -1
            for i in range(len(self.player_list)):
                if chebyshev_distance(game_state.player_state_list[my_player_index].position, game_state.player_state_list[self.player_list[i]].position) <= 2:
                    if game_state.player_state_list[self.player_list[i]].health >= max_health:
                        max_health_enemy = self.player_list[i]
                        max_health = game_state.player_state_list[self.player_list[i]].health

            if max_health_enemy == -1:
                return self.player_list[0]
            else:
                return max_health_enemy
        else:
            if my_player_index in self.player_list:
                self.player_list.pop(my_player_index)
            min_health = 9
            min_health_enemy = -1
            for i in range(len(self.player_list)):
                if chebyshev_distance(game_state.player_state_list[my_player_index].position, game_state.player_state_list[self.player_list[i]].position) <= 2:
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
        if self.archer_count(game_state, my_player_index):
            if self.at_spawn(game_state, my_player_index) and game_state.player_state_list[my_player_index].gold >= 8:
                return Item.SHIELD
            return Item.NONE
        else:
            if self.at_spawn(game_state, my_player_index) and game_state.player_state_list[my_player_index].gold >= 5:
                return Item.STRENGTH_POTION
            return Item.NONE
     