from game_states import GameStates
from entity import get_blocking_entities_at_location
from game_messages import Message
import tdl


"""
File contain all function that interact with keys in all game situation
"""

def handle_keys(user_input, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(user_input)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(user_input)
    elif game_state == GameStates.SHOW_INVENTORY:
        return handle_inventory_keys(user_input)
    return {}


def handle_inventory_keys(user_input):
    if not user_input.char:
        return {}

    index = ord(user_input.char) - ord('a')

    if index >= 0:
        return {'index_inventory': index}

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Exit the game
        return {'exit': True}

    return {}


def handle_player_dead_keys(user_input):
    key_char = user_input.char

    if key_char == 'i':
        return {'show_inventory': True}

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def handle_player_turn_keys(user_input):
    # Movement keys
    key_char = user_input.char
    if user_input.key == 'UP':
        return {'move': (0, -1)}
    elif user_input.key == 'DOWN':
        return {'move': (0, 1)}
    elif user_input.key == 'LEFT':
        return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT':
        return {'move': (1, 0)}

    if key_char == 'g':
        return {'pickup' : True}
    elif key_char == 'i':
        return {'show_inventory': True}

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def main_handle(game_state, previous_game_state, player, game_map, fov_recompute, entities, message_log, colors):
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
            break
    else:
        user_input = None

    if not user_input:
        return None
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
                    pickup_results = entity.item.pick_up(player, entity)
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

    return game_state, player_turn_results, fov_recompute
