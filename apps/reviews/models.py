from django.db import models
from django.contrib.auth.models import User
from apps.books.models import Book

class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'user']  # One review per user per book
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
    def vote_count(self):
        return self.votes.filter(vote_type=1).count()
