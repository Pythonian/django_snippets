from django.urls import path

from ..views import bookmarks

app_name = 'bookmarks'

urlpatterns = [
    path('',
         bookmarks.user_bookmarks,
         name='user'),

    path('<int:snippet_id>/add/',
         bookmarks.add_bookmark,
         name='add'),

    path('<int:snippet_id>/delete/',
         bookmarks.delete_bookmark,
         name='delete'),
]
