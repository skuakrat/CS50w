from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    url = models.URLField(blank=True, max_length=2000)


class Province(models.Model):
    name_en = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name_en}"

class Type(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type}"
    
class Breed(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    breed = models.CharField(max_length=255)
    

    def __str__(self):
        return f"{self.type} - {self.breed}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    type = models.ForeignKey("Type", on_delete=models.CASCADE, related_name="types")
    breed = models.ForeignKey("Breed", on_delete=models.CASCADE, related_name="breeds", blank=True, null=True)
    province = models.ForeignKey("Province", on_delete=models.CASCADE, related_name="provinces", blank=True, null=True)
    address = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    url = models.URLField(blank=True, max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="posts_liked", blank=True)
    status = models.IntegerField(default=1)
    adopter = models.ForeignKey("User", on_delete=models.CASCADE, related_name="adopters", blank=True, null=True)
    comments = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="comments", blank=True, null=True)

    def serialize(self):
        likes_count = len(self.likes.all()) if self.likes else 0
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likers": [user.username for user in self.likes.all()],
            "likes": likes_count,
        }
    
    def __str__(self):
        return f"({self.id}) - {self.user} posted {self.body}"
    

    
class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="commentposts")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="commenters")
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return f"{self.user} commented {self.body}"
    
class Dm(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="dmers")
    to = models.ForeignKey("User", on_delete=models.CASCADE, related_name="dmeds")
    timestamp = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=600, blank=True)
    body = models.TextField()
    read = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} wrote to {self.to} - '{self.body} on {self.timestamp}'"