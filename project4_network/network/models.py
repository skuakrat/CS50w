from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    puser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    ppost = models.TextField(max_length=1000)
    pdate = models.DateTimeField(auto_now_add=True, editable=False)
    plikes = models.ManyToManyField(User, blank=True, related_name="likers")

    def serialize(self):
        if self.puser in self.plikes.all():
            self.plike = "1"
        if self.puser not in self.plikes.all():
            self.plike = "0"

        return {
            "id": self.id,
            "puser": self.puser.username,
            "ppost": self.ppost,
            "pdate": self.pdate.strftime("%b %d %Y, %I:%M %p"),
            "plikes": [user.username for user in self.plikes.all()],
            "myplike": self.plike,
            "plikesnum": self.plikes.count(),
        }

    def __str__(self):
        return f"Post#{self.id} listed by {self.puser}"


class Follow(models.Model):
    fuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ffuser")
    ffollowers = models.ManyToManyField(User, blank=True, related_name="ferslists")
    ffollowings = models.ManyToManyField(User, blank=True, related_name="fingslists")

    def serialize(self):

        return {
            "fuser": self.fuser.username,
            "femail": self.fuser.email,
            "ffollowers": [user.username for user in self.ffollowers.all()],
            "ffollowings": [user.username for user in self.ffollowings.all()],
            "ffollowersnum": self.ffollowers.count(),
            "ffollowingsnum": self.ffollowings.count(),
        }


    def __str__(self):
        return f"{self.fuser} follow status"
