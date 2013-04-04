from django.db import models
from django.contrib.auth.models import User
import random






class Game(models.Model):
    created = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(User, null=True)
    turn = models.ForeignKey(User, related_name='turn+', null=True)
    completed = models.BooleanField(default=False)
    played_out = models.TextField(null=True, blank=True)



    class Meta():
        ordering = ['pk']



    def __unicode__(self):
        return 'Game ' + str(self.id)


    def generate(self):
        choices = 'abcdefghijklmnopqrstuvwxyz'

        for i in range(25):
            randomletter = choices[random.randrange(0,25)]
            l = Letter(character=randomletter, game=self)
            l.save()

        return self


    def next_turn(self):
        p = self.players.all()

        self.turn = p[0] if self.turn == p[1] else p[1]

        self.save()
        
        return self 

    # TODO:
    # def to_json()





class Letter(models.Model):
    character = models.CharField(max_length=1)
    game = models.ForeignKey(Game)
    locked = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, blank=True)


    def __unicode__(self):
        return self.character;


    def get_owner(self):
        if self.owner:
            return self.owner.username
        else:
            return False


    class Meta:
        ordering = ['pk',]


    # TODO:
    # def to_json()
