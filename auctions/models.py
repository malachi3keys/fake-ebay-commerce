from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Tag(models.Model):
    post_tag = models.CharField(max_length=20)
        
    def __str__(self):
        return f"{self.post_tag}"
        

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postuser")
    post_title = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=500)
    bid_start = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='images/', max_length=200, null=True, blank=True)
    list_tag = models.ManyToManyField(Tag, related_name="category",blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.post_title}"


class Bid(models.Model):
    dollar = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")

    def __str__(self):
        return f"{self.dollar}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replyuser")
    body = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.listing}"
        

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watcher")
    listing = models.ManyToManyField(Listing, blank=True, related_name="watchlisting")

    def __str__(self):
        return f"{self.user}"