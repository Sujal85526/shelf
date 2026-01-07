from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Vote
from apps.reviews.models import Review

@login_required
def vote_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    vote = Vote.objects.filter(user=request.user, review=review).first()
    
    if vote:
        vote.delete()  # Toggle OFF
    else:
        Vote.objects.create(
            user=request.user, 
            review=review, 
            vote_type='up'
        )  # Toggle ON
    
    return redirect('book_detail', pk=review.book.pk)

