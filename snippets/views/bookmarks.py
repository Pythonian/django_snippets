from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from ..models import Bookmark, Snippet


@login_required
def add_bookmark(request, snippet_id):
    """
    Function to let a user add a snippet to his bookmark.
    Checks whether the user already has a bookmark to this
    snippet, otherwise creates one.
    """
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    try:
        Bookmark.objects.get(
            user__pk=request.user.id,
            snippet__pk=snippet.id)
    except Bookmark.DoesNotExist:
        bookmark = Bookmark.objects.create(
            user=request.user,
            snippet=snippet)
    messages.success(request, 'You have bookmarked this snippet')
    return HttpResponseRedirect(snippet.get_absolute_url())


@login_required
def delete_bookmark(request, snippet_id):
    """
    Filter() to create a queryset of any bookmark that match the user
    and this bookmark then call the delete() method on the queryset.
    """
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if request.method == 'POST':
        Bookmark.objects.filter(
            user__pk=request.user.id,
            snippet__pk=snippet.id).delete()
        messages.success(
            request, 'You have removed this snippet from your bookmark')
        return HttpResponseRedirect(snippet.get_absolute_url())
    else:
        return render(request, 'bookmarks/confirm_bookmark_delete.html',
                      {'snippet': snippet})


def user_bookmarks(request):
    """ List the current user's bookmarks """
    bookmarks = Bookmark.objects.filter(user__pk=request.user.id)

    template_name = 'bookmarks/user_bookmarks.html'
    context = {'bookmarks': bookmarks}

    return render(request, template_name, context)
