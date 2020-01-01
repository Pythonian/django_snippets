from django.urls import path

from ..views import popular

app_name = 'popular'

urlpatterns = [
    path('authors/',
         popular.top_authors,
         name='authors'),

    path('languages/',
         popular.top_languages,
         name='languages'),

    path('bookmarks/',
         popular.most_bookmarked,
         name='bookmarked'),

    # path('rated/',
    #      popular.top_rated,
    #      name='top_rated'),
]
