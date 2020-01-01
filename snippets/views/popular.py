from django.shortcuts import render

from ..models import Snippet, Language


def top_authors(request):
    """ A view to list out the top authors. """
    top_authors = Snippet.objects.top_authors()

    template_name = 'popular/top_authors.html'
    context = {'top_authors': top_authors}

    return render(request, template_name, context)


def top_languages(request):
    """ A view to list out the top languages """
    top_languages = Language.objects.top_languages()

    template_name = 'popular/top_languages.html'
    context = {'top_languages': top_languages}

    return render(request, template_name, context)


def most_bookmarked(request):
    """ A view to list out the most bookmarked snippets by users. """
    bookmarks = Snippet.objects.most_bookmarked()

    template_name = 'popular/most_bookmarked.html'
    context = {'bookmarks': bookmarks}

    return render(request, template_name, context)


# def top_tags(request):
#    writing a view that lists tags ordered by the number of snippets that use them
#     return object_list(
#         request,
#         queryset=Snippet.objects.top_tags(),
#         template_name='cab/tag_list.html',
#         paginate_by=20,
#     )


# def top_rated(request):
#     queryset = Snippet.objects.top_rated()
#     return month_object_list(
#         request,
#         queryset=queryset,
#         template_name='cab/top_rated.html',
#         paginate_by=20,
#     )
