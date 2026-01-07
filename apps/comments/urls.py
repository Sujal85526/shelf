from django.urls import path
from . import views

urlpatterns = [
    # Top level comment
    path('review/<int:review_pk>/comment/', views.comment_create, name='comment_create'),
    # Reply to specific comment
    path('review/<int:review_pk>/comment/<int:parent_pk>/', views.comment_create, name='comment_reply'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
