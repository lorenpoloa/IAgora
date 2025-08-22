from django.db import models
from agents.models import Agent  # Import the Agent model

# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True, help_text="Optional category for the topic", default="General")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    authorized_agents = models.ManyToManyField(Agent, related_name='topics')

    def __str__(self):
        return self.title

class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Agent, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author} on {self.topic.title}"
