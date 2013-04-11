import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from letterpress.games.models import Game, Letter
from letterpress.users.utilities import get_gravatar
from letterpress.api.utilities import game_to_dict
from pprint import pprint
from sowpods.verify_word import verify_word



def game_list(request, pk=None):
    """
    retrieve a list of games or details about a particular game
    """
    games = Game.objects.all()

    data = []

    for game in games:
        data.append( game_to_dict(game) )

    return HttpResponse(json.dumps(data), mimetype="application/json")





# TODO:
# this disaster needs to be cleaned up
def game_detail(request, pk):
    """
    details about a particular game
    """
    if (request.method == 'PUT'):
        game = get_object_or_404(Game, pk=pk)

        if request.user == game.turn:
            letters_set = game.letter_set.all()
            request_json = json.loads(request.body)
            played_letters = []

            # iterate over the letters and pluck the ones that have been played
            for index, letter in enumerate(request_json['letters']):
                if letter['inPlay'] != False:
                    # pull the character from the index of the letter set on the server
                    # rather than to client-side request to formulate the word.
                    played_letters.append(
                        {
                            'id': letter['id'],
                            'character': letters_set.get(pk=letter['id']).character,
                            'position': letter['inPlay']
                        }
                    )

            # sort the letters by their position in the play view
            played_letters = sorted(played_letters, key=lambda letter: letter['position'])

            # create a string from the letters
            word = ''.join([letter['character'] for letter in played_letters])

            # make sure the word hasn't been used before
            word_is_new = not game.been_played(word)

            # check the dictionary
            in_dictionary = verify_word(word)
            

            if in_dictionary and word_is_new:
                for letter in played_letters:
                    l = letters_set.get(pk=letter['id'])
                    # TODO
                    # use a key instead of a plain email address
                    # make sure the letter isn't locked
                    # don't identify by the letter id from the request json
                    if not l.locked:
                        l.owner = game.players.get(username=request_json['turn'])
                        l.save()

                # update locked letters
                i = 0
                for letter in letters_set:
                    if letter.owner:
                        north = True if (i < 5) or (i > 4 and letters_set[i - 5].owner == letter.owner) else False
                        east = True if (i % 5 == 4) or (i % 5 != 4 and letters_set[i + 1].owner == letter.owner) else False
                        south = True if (i > 19) or (i < 20 and letters_set[i + 5].owner == letter.owner) else False
                        west = True if (i % 5 == 0) or (i % 5 != 0 and letters_set[i - 1].owner == letter.owner) else False

                        letter.locked = (north and south and east and west)
                        letter.save()


                    i += 1

                game.played_out = (game.played_out if game.played_out != None else '') + word + ' '
                game.next_turn()

            updated = in_dictionary and word_is_new
        else:
            updated = False

        if not updated:
            return HttpResponse("Error", status=422)


    game = get_object_or_404(Game, pk=pk)

    data = game_to_dict(game)

    return HttpResponse(json.dumps(data), mimetype="application/json")
