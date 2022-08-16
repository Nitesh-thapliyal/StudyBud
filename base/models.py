from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Database creation happens here

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# class name represent table name and variable inside it are columns in table
# models by default has id generated for them 
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    # below class specify that the newest room should be displayed first in the home page
    class Meta:
        ordering = ['-updated', 'created'] #here dash is for newest item first that is descending order

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # one to many relationship
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #here casecade specify that if the room gets deleted then all its children also gets deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body[0:50]