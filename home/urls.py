from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create/', views.CreatePostView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('update/<slug:slug>/', views.PostUpdateView.as_view(), name='post_update'),
    path('delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    path('category/<slug:category_slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),

]