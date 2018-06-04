
import tdl
from entity import Entity
from render_functions import render_all, clear_all,RenderOrder
from game_states import GameStates
from death_functions import kill_monster, kill_player
from game_messages import MessageLog
from config import Config
from map_utils import GameMap, make_map
from components.fighter import Fighter
from components.inventory import Inventory
from handle import main_handle

def main():
    """
    Main loop of the game.
    Some initialization before loop
    """
    fov_recompute = True
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    inventory_component = Inventory(26)
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    entities = [player]
    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(Config.screen_width, Config.screen_height, title='Roguelike 3000')
    con = tdl.Console(Config.screen_width, Config.screen_height)
    panel = tdl.Console(Config.screen_width, Config.panel_height)

    game_map = GameMap(Config.map_width, Config.map_height)
    make_map(game_map, Config.max_rooms, Config.room_min_size, Config.room_max_size, Config.map_width, Config.map_height,
             player, entities, Config.max_monsters_per_room, Config.colors)
    message_log = MessageLog(Config.message_x, Config.message_width, Config.message_height)


    while not tdl.event.is_window_closed() and game_state != GameStates.PLAYER_DEAD:
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=Config.fov_algorithm, radius=Config.fov_radius, light_walls=Config.fov_light_walls)

        render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log, Config.screen_width,
                   Config.screen_height, Config.bar_width, Config.panel_height, Config.panel_y, Config.colors, game_state)

        tdl.flush()
        clear_all(con, entities)
        fov_recompute = False
        res = main_handle(game_state, previous_game_state, player, game_map, fov_recompute, entities, message_log, Config.colors)
        if res is None:
            continue

        if res == True:
            return True
        game_state, player_turn_results, fov_recompute = res

        """
        Find out results of players move 
        """
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_droped = player_turn_result.get('item_droped')
            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity, Config.colors)
                else:
                    message = kill_monster(dead_entity, Config.colors)

                message_log.add_message(message)

            if item_droped:
                e = Entity(player.x, player.y, item_droped.short, color=Config.colors.get("violet"), name="Armor",
                           render_order=RenderOrder.ITEM, item=item_droped)
                entities.append(e)
            if item_added:
                entities.remove(item_added)

        """
        Enemy movement 
        """
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, game_map, entities)
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity, Config.colors)
                            else:
                                message = kill_monster(dead_entity, Config.colors)

                            message_log.add_message(message)

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()