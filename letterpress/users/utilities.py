import urllib, hashlib

from django.contrib.auth.models import User



def get_gravatar(user):
    # Set your variables here
    email = user.email
    default = "http://cdn.cutestpaw.com/wp-content/uploads/2012/04/l-my-first-kitten.jpg"
    size = 100
     
    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

    return gravatar_url