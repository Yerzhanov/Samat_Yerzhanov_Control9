from django.urls import path
from posts.views import post_create, feed, like_post, PostDetailView, PostUpdateView, PostDeleteView, \
    post_list_and_create

urlpatterns = [
    path('create', post_create, name='create'),
    path('feed', feed, name='feed'),
    path('like', like_post, name='like'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post_view'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),

    path('main/', post_list_and_create, name='main_page'),

    ]
