from django.urls import path

from . import views
app_name = "posts"
urlpatterns = [
    path("group/<slug:slug>/", views.group_posts, name="group_posts"),
    path("", views.index, name="posts_index"),
    path("new/", views.new_post, name="new_post"),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path(
        '<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    )
]
