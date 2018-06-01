import tdl
from handle import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import render_all, clear_all,RenderOrder
from map_utils import GameMap, make_map
from game_states import GameStates
from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from game_messages import MessageLog, Message
from components.inventory import Inventory
from components.item import  Item

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 43

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 3


    fov_algorithm = 'BASIC'
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50),
        'desaturated_green': (63, 127, 63),
        'darker_green': (0, 127, 0),
        'dark_red': (191, 0, 0),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'orange': (255, 127, 0),
        'light_red': (255, 114, 114),
        'darker_red': (127, 0, 0),
        'violet': (127, 0, 255),
        'yellow': (255, 255, 0),
        'blue': (0, 0, 255),
        'green': (0, 255, 0)
    }

    inventory_component = Inventory(26)
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    entities = [player]
    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(screen_width, screen_height, title='Roguelike 3000')
    con = tdl.Console(screen_width, screen_height)
    panel = tdl.Console(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
             max_monsters_per_room, colors)
    fov_recompute = True
    message_log = MessageLog(message_x, message_width, message_height)
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    while not tdl.event.is_window_closed() and game_state != GameStates.PLAYER_DEAD:
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls)

        render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log, screen_width,
                   screen_height, bar_width, panel_height, panel_y, colors, game_state)

        tdl.flush()
        clear_all(con, entities)
        fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if not user_input:
            continue
        action = handle_keys(user_input, game_state)
        player_turn_results = []
        if game_state == GameStates.PLAYERS_TURN:
            if "move" in action:
                move = action["move"]
                destination_x = player.x + move[0]
                destination_y = player.y + move[1]

                if game_map.walkable[destination_x, destination_y]:
                    target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)
                    else:
                        player.move(move[0], move[1])
                        fov_recompute = True
            elif "pickup" in action:
                for entity in entities:
                    if entity.item and entity.x == player.x and entity.y == player.y:
                        pickup_results = player.inventory.add_item(entity, colors)
                        player_turn_results.extend(pickup_results)
                        break
                else:
                    message_log.add_message(Message('There is nothing here to pick up.', colors.get('yellow')))

            game_state = GameStates.ENEMY_TURN

        if "show_inventory" in action:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if "index_inventory" in action and previous_game_state != GameStates.PLAYER_DEAD:
            index = action["index_inventory"]
            if index < len(player.inventory.items):
                item = player.inventory.items[index]
                player_turn_results.extend(item.item.use(player))
                player.inventory.remove(index)
                game_state = previous_game_state

        if "exit" in action:
            if game_state == GameStates.SHOW_INVENTORY:
                game_state = previous_game_state
            else:
                return True

        if "fullscreen" in action:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity, colors)
                else:
                    message = kill_monster(dead_entity, colors)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

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
                                message, game_state = kill_player(dead_entity, colors)
                            else:
                                message = kill_monster(dead_entity, colors)

                            message_log.add_message(message)

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()