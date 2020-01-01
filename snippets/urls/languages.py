from django.urls import path

from ..views import languages

app_name = 'languages'

urlpatterns = [
    path('',
         languages.language_list,
         name='list'),

    path('<slug:slug>/',
         languages.language_detail,
         name='detail'),
]
