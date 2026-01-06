from django.db import models
from django.contrib.auth.models import User
from apps.reviews.models import Review

class Vote(models.Model):
    VOTE_CHOICES = [(1, 'Upvote'), (-1, 'Downvote')]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.IntegerField(choices=VOTE_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'user']  # One vote per user per review
    
    def __str__(self):
        return f"{self.user.username} voted on {self.review}"
