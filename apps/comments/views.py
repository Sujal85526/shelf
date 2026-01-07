from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from .forms import CommentForm
from apps.reviews.models import Review

@login_required
def comment_create(request, review_pk, parent_pk=None):
    review = get_object_or_404(Review, pk=review_pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            if parent_pk:
                parent_comment = get_object_or_404(Comment, pk=parent_pk)
                comment.parent = parent_comment
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('book_detail', pk=review.book.pk)
    else:
        form = CommentForm()
    return render(request, 'comments/comment_form.html', {
        'form': form, 
        'review': review,
        'parent_pk': parent_pk
    })

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        messages.error(request, 'You can only delete your own comments!')
        return redirect('book_detail', pk=comment.review.book.pk)
    
    book_pk = comment.review.book.pk
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('book_detail', pk=book_pk)
    return render(request, 'comments/comment_confirm_delete.html', {'comment': comment})
