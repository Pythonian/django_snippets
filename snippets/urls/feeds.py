from django.urls import path

from .. import feeds

app_name = 'feeds'

urlpatterns = [
    path('author/<username>/',
         feeds.SnippetsByAuthorFeed(), name='author'),

    path('language/<slug:slug>/',
         feeds.SnippetsByLanguageFeed(), name='language'),

    path('latest/',
         feeds.LatestSnippetsFeed(), name='latest'),

    # path('tag/<slug:slug>/',
    #      feeds.SnippetsByTagFeed(), name='feed_tag'),
]
