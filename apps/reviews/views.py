from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from apps.books.models import Book

@login_required
def review_create(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    
    # Check if user already reviewed this book
    if Review.objects.filter(book=book, user=request.user).exists():
        messages.error(request, 'You have already reviewed this book!')
        return redirect('book_detail', pk=book_pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('book_detail', pk=book_pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'book': book})

@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        messages.error(request, 'You can only edit your own reviews!')
        return redirect('book_detail', pk=review.book.pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('book_detail', pk=review.book.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form, 'book': review.book, 'review': review})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        messages.error(request, 'You can only delete your own reviews!')
        return redirect('book_detail', pk=review.book.pk)
    
    book_pk = review.book.pk
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('book_detail', pk=book_pk)
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})
