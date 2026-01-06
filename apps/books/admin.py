from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'submitted_by', 'created_at']
    list_filter = ['genre', 'created_at']
    search_fields = ['title', 'author', 'isbn']
