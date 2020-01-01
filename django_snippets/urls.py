from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookmarks/', include('snippets.urls.bookmarks',
                               namespace='bookmarks')),
    path('feeds/', include('snippets.urls.feeds', namespace='feeds')),
    path('languages/', include('snippets.urls.languages',
                               namespace='languages')),
    path('popular/', include('snippets.urls.popular', namespace='popular')),
    path('', include('snippets.urls.snippets', namespace='snippets')),
]
