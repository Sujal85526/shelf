from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:book_pk>/review/', views.review_create, name='review_create'),
    path('review/<int:pk>/edit/', views.review_update, name='review_update'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
]
