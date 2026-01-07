from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Book
from .forms import BookForm

def book_list(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'query': query})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    
    # BUILD TREE STRUCTURE - NO MODEL ASSIGNMENT
    for review in reviews:
        # Get top-level comments
        top_level_comments = review.comments.filter(parent__isnull=True).order_by('created_at')
        
        # For each top-level comment, find its replies
        comment_tree = []
        all_comments = review.comments.all()
        
        for comment in top_level_comments:
            # Create dict with comment and its replies
            tree_item = {
                'comment': comment,
                'replies': [c for c in all_comments if c.parent == comment]
            }
            comment_tree.append(tree_item)
        
        review.comment_tree = comment_tree
    
    return render(request, 'books/book_detail.html', {'book': book, 'reviews': reviews})

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.submitted_by = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.submitted_by != request.user:
        messages.error(request, 'You can only edit your own books!')
        return redirect('book_detail', pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'book': book})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.submitted_by != request.user:
        messages.error(request, 'You can only delete your own books!')
        return redirect('book_detail', pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
