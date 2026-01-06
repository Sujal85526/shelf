from django.contrib import admin
from .models import Vote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
