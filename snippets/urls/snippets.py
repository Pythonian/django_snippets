from django.urls import path

from ..views import snippets

app_name = 'snippets'

urlpatterns = [
    path('',
         snippets.snippet_list,
         name='list'),

    path('add/',
         snippets.snippet_add,
         name='add'),

    path('<int:snippet_id>/',
         snippets.snippet_detail,
         name='detail'),

    path('<int:snippet_id>/edit/',
         snippets.snippet_edit,
         name='edit'),

    path('<int:snippet_id>/download/',
         snippets.snippet_download,
         name='download'),

    path('<int:snippet_id>/raw/',
         snippets.snippet_raw,
         name='raw'),

    path('<int:snippet_id>/flag/',
         snippets.snippet_flag,
         name='flag'),

    path('<int:snippet_id>/rate/',
         snippets.snippet_rate,
         name='rate'),

]
