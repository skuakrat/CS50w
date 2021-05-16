from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Item(models.Model):
    iuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    item = models.CharField(max_length=64)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="itemcategory")
    iprice = models.DecimalField(max_digits=16, decimal_places=2)
    ibid = models.DecimalField(max_digits=16, decimal_places=2)
    idate = models.DateTimeField(default=now, editable=False)
    url = models.URLField(blank=True)
    des = models.TextField(blank=True)
    status = models.IntegerField()
    iwatch = models.ManyToManyField(User, blank=True, related_name="iwatchlists")

    def __str__(self):
        return f"{self.item} listed by {self.iuser}"

class Bid(models.Model):
    buser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidowner")
    bitem =  models.ForeignKey(Item, on_delete=models.CASCADE, related_name="biditem")
    bprice = models.DecimalField(max_digits=16, decimal_places=2)
    bdate = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.buser} bidded on {self.bitem} for {self.bprice}, {self.bdate}"

class Comment(models.Model):
    cuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    citem = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="commentitem")
    cdate = models.DateTimeField(default=now, editable=False)
    comment = models.TextField()

    def __str__(self):
        return f"{self.cuser} commented on {self.citem} at {self.cdate}"

class Watchlist(models.Model):
    wuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    witem = models.ManyToManyField(Item, blank=True, related_name="watchlists")

    def __str__(self):
        return f"{self.wuser} watchlist"