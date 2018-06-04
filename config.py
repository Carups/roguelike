class Config:
    """
    Class contain all constant values of the game
    """
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

