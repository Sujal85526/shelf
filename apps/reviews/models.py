from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from apps.books.models import Book

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.book.pk})

    # 🆕 PHASE 6 VOTING - NO IMPORTS NEEDED
    def get_helpful_count(self):
        """Safe count - works even without Vote model"""
        try:
            return self.vote.filter(vote_type='up').count()
        except:
            return 0

    def get_vote_for_user(self, user):
        """Safe user vote lookup"""
        if user and user.is_authenticated:
            try:
                return self.vote_set.get(user=user)
            except:
                return None
        return None

    @property
    def helpful_count(self):
        return self.votes.filter(vote_type='up').count()

    @property
    def vote_for_user(self):
        # Get user from request context in view
        request = getattr(self, 'request', None)
        user = getattr(request, 'user', None) if request else None
        return self.get_vote_for_user(user)
