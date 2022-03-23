from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction",default='')
    category = models.CharField(max_length=64, blank=True, default='')
    name = models.CharField(max_length=64)
    bid = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidd")
    howmuch = models.FloatField()
    whichListing = models.ForeignKey(AuctionListings,on_delete=models.CASCADE, related_name="offereds")

    def __str__(self):
        return f"{self.person} offers {self.howmuch} to {self.whichListing}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    content = models.CharField(max_length=128)
    commentedListing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="listingcomments")

    def __str__(self):
        return f"{self.commenter}: {self.content}"