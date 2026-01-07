from django.db import models
from django.contrib.auth.models import User

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey('reviews.Review', on_delete=models.CASCADE, related_name='votes')  # ← STRING FIX
    vote_type = models.CharField(max_length=10, choices=[('up', 'Helpful'), ('down', 'Not helpful')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'review']
    
    def __str__(self):
        return f"{self.user.username} voted {self.vote_type}"
