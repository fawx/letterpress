import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from letterpress.games.models import Game, Letter
from letterpress.users.utilities import get_gravatar
from pprint import pprint
from sowpods.verify_word import verify_word




def list(request):
    return render(request, 'games/games_list.html')




def create(request):
    # new game creation page
    if request.method == 'GET':
        users = User.objects.all().exclude(pk__exact=request.user.pk)
        return render(request, 'games/games_create.html', { 'users': users })

    # create the game and redirect to home page
    # TODO:
    # game creation confirmation
    # send an invitation to opponent
    if request.method == 'POST':
        g = Game()
        g.save()

        g.players.add(request.user)
        g.players.add(User.objects.get(username__iexact=request.POST['username']))
        g.turn = request.user
        g.generate()
        g.save()

        return redirect('letterpress.games.views.list')






def api_game_list(request):
    """
    retrieve a list of games
    """
    games = Game.objects.all()

    data = []

    for game in games:
        # todo
        # move to model, replace with to_json
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

        data.append({
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
        })

    return HttpResponse(json.dumps(data), mimetype="application/json")





# TODO:
# clean up everything below this line
# build some decent errors
def api_game_detail(request, pk):
    """
    details about a particular game
    """
    if (request.method == 'PUT'):
        updated = game_update(request, pk)
        if not updated:
            return HttpResponse("Error", status=422)


    game = get_object_or_404(Game, pk=pk)
    players = game.players.all()
    letters_set = game.letter_set.all()
    letters = []

    # TODO:
    # move all this to the model
    for letter in letters_set:
        letters.append({
            'id': letter.pk,
            'character': letter.character,
            'locked': letter.locked,
            'owner': letter.get_owner()
        })

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
                'points': len(letters_set.filter(owner__exact=players[0]))
            },
            {
                'username': game.players.all()[1].username,
                'gravatar': get_gravatar(game.players.all()[1]),
                'points': len(letters_set.filter(owner__exact=players[1]))
            }
        ]
    }

    return HttpResponse(json.dumps(data), mimetype="application/json")




def game_update(request, pk):
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
        word = ''.join([letter['character'] for letter in played_letters])
        word_is_valid = verify_word(word)

        if word_is_valid:
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

        return word_is_valid
    else:
        return False
