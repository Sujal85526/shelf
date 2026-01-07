from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from apps.books.models import Book
from apps.reviews.models import Review

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    
    context = {
        'profile_user': user,
        'user_books': Book.objects.filter(submitted_by=user)[:6],
        'user_reviews': Review.objects.filter(user=user).select_related('book')[:8],
        'total_books': Book.objects.filter(submitted_by=user).count(),
        'total_reviews': Review.objects.filter(user=user).count(),
        'total_votes': user.vote_set.count(),
    }
    return render(request, 'profiles/profile_detail.html', context)
