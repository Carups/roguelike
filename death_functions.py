from game_states import GameStates
from render_functions import  RenderOrder
from game_messages import Message


def kill_player(player, colors):
    """
    :param player: main entity for player
    :param colors: colors for players corpse
    :return: Message about players death and new GameStatus
    """
    player.char = '%'
    player.color = colors.get('dark_red')

    return Message('You died!', colors.get('red')), GameStates.PLAYER_DEAD


def kill_monster(monster, colors):
    """
    :param monster: entity for mob
    :param colors: colors for mob corpse
    :return: Message about mob death
    """
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), colors.get('orange'))

    monster.char = '%'
    monster.color = colors.get('dark_red')
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message