from game_states import GameStates


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
