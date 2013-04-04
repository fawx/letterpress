import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from letterpress.users.utilities import get_gravatar


def home(request):
    return render(request, 'games/games.html')


    
def create(request):
    users = User.objects.all()

    errors = {}
    postdata = []

    if request.method == 'POST':
        postdata = request.POST

        # unique username?
        if len(users.filter(username__iexact=request.POST['username'])) > 0:
            errors['username'] = True

        # unique email?
        if len(users.filter(email__iexact=request.POST['email'])) > 0:
            errors['email'] = True

        # passwords match?
        if request.POST['password'] != request.POST['password_confirm']:
            errors['password_confirm'] = True

        # password is long enough?
        if request.POST['password'] == request.POST['password_confirm'] and len(request.POST['password']) < 6:
            errors['password_length'] = True

        # create the user!
        if len(errors) == 0:
            User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            return redirect('letterpress.users.views.create_success')


    return render(request, 'accounts/create.html', { 'users': users, 'errors': errors, 'postdata': postdata })



def create_success(request):
    return render(request, 'accounts/create_success.html')






def api_user_current(request):
    user = get_object_or_404(User, pk=request.user.pk)

    data = {
        'id': user.pk,
        'username': user.username,
        'email': user.email,
        'gravatar': get_gravatar(user)
    }

    return HttpResponse(json.dumps(data), mimetype="application/json")
