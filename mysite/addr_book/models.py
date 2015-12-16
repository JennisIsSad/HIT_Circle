# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
#import datetime
class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)
        
class Profile(object):
    __metaclass__ = ProfileBase

class MyProfile(Profile):
    nickname = models.CharField(max_length = 255, blank = True)
    realname = models.CharField(max_length = 255, null = True, blank = True)
    studynumber = models.CharField(max_length = 30, blank = True)
    profession = models.CharField(max_length = 255, blank = True)
    sex = models.BooleanField(default = True)

class Tweet(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length = 140)
    tweet_time = models.DateTimeField(auto_now_add=True)
         
    def __unicode__(self):
        return self.content

class FriendshipManager(models.Manager):
    
    def friends_for_user(self, user):
        friends = []
        for friendship in self.filter(from_user=user).select_related(depth=1):
            friends.append({"friend": friendship.to_user, "friendship": friendship})
        for friendship in self.filter(to_user=user).select_related(depth=1):
            friends.append({"friend": friendship.from_user, "friendship": friendship})
        return friends
    
    def are_friends(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).count() > 0:
            return True
        if self.filter(from_user=user2, to_user=user1).count() > 0:
            return True
        return False
    
    def remove(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            friendship = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            friendship = self.filter(from_user=user2, to_user=user1)
        friendship.delete()

class Friendship(models.Model):
    """
    A friendship is a bi-directional association between two users who
    have both agreed to the association.
    """
    
    to_user = models.ForeignKey(User, related_name="friends")
    from_user = models.ForeignKey(User, related_name="_unused_")
    # @@@ relationship types
    added = models.DateField(default=datetime.date.today)
    objects = FriendshipManager()
    
    class Meta:
        unique_together = (('to_user', 'from_user'),)
