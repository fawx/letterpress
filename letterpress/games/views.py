from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from letterpress.games.models import Game, Letter
from letterpress.users.utilities import get_gravatar



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
