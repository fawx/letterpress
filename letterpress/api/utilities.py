import json
from letterpress.users.utilities import get_gravatar




def game_to_dict(game):
    """
    convert a game to a normal dictionary so we can serialize it with json in the api
    """
    letters_set = game.letter_set.all()
    letters = []

    i = 0;
    for letter in letters_set:
        letters.append({
            'id': letter.pk,
            'character': letter.character,
            'locked': letter.locked,
            'owner': letter.get_owner()
        })

        i = i + 1

    data = {
        'id': game.pk,
        'turn': game.turn.username,
        'played_out': game.played_out,
        'completed': game.completed,
        'letters': letters,
        'players': [
            {
                'username': game.players.all()[0].username,
                'gravatar': get_gravatar(game.players.all()[0]),
                'points': len(game.letter_set.filter(owner__exact=game.players.all()[0]))
            },
            {
                'username': game.players.all()[1].username,
                'gravatar': get_gravatar(game.players.all()[1]),
                'points': len(game.letter_set.filter(owner__exact=game.players.all()[1]))
            }
        ]
    }

    return data
