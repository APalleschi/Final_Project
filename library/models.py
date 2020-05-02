from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # librarycard = models.ManyToManyField("Listing", related_name="cards")
    loan = models.ManyToManyField("Listing", related_name="loans")

class Section(models.Model):

    class Meta:
        verbose_name_plural = "sections"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Listing(models.Model):
    active = models.BooleanField(default=True)
    restricted = models.BooleanField(default=False)
    section = models.ForeignKey("Section", on_delete=models.SET_NULL, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    seller = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(blank=True)
    commenter = models.ForeignKey("User", on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.content