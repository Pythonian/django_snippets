from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from snippets.forms import SnippetFlagForm, SnippetForm
from snippets.models import Rating, Snippet, SnippetFlag


def snippet_list(request):
    """
    Returns a snippet list page.

    Template: ``snippets/snippet_list.html``
    Context:
        snippet_list
            Snippet object list
    """
    snippet_list = Snippet.objects.all()

    template_name = 'snippets/snippet_list.html'
    context = {'snippet_list': snippet_list}

    return render(request, template_name, context)


def snippet_detail(request, snippet_id):
    snippet_detail = get_object_or_404(Snippet, pk=snippet_id)

    template_name = 'snippets/detail.html'
    context = {'snippet': snippet_detail}

    return render(request, template_name, context)


def snippet_download(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    response = HttpResponse(snippet.code, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s.%s' % \
        (snippet.id, snippet.language.file_extension)
    response['Content-Type'] = snippet.language.mime_type
    return response


def snippet_raw(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    response = HttpResponse(snippet.code, content_type='text/plain')
    response['Content-Disposition'] = 'inline'
    return response


@login_required
def snippet_add(request):
    """
    Returns a form page to create snippet.

    Templates: ``snippets/snippet_form.html``
    Context:
        form
            SnippetForm object
        add
            Boolean flag
    """
    if request.method == 'POST':
        form = SnippetForm(data=request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            messages.success(
                request, 'Your snippet has been successfully saved')
            return HttpResponseRedirect(snippet.get_absolute_url())
    else:
        form = SnippetForm()

    template_name = 'snippets/snippet_form.html'
    context = {'form': form, 'add': True}

    return render(request, template_name, context)


@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if request.user.id != snippet.author.id or not request.user.is_active:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = SnippetForm(data=request.POST, instance=snippet)
        if form.is_valid():
            snippet = form.save()
            messages.success(
                request, 'Your snippet has been successfully edited')
            return HttpResponseRedirect(snippet.get_absolute_url())
    else:
        form = SnippetForm(instance=snippet)

    template_name = 'snippets/snippet_form.html'
    context = {'form': form, 'add': False}

    return render(request, template_name, context)


@login_required
def snippet_rate(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    # Verify the acceptable query string is present or redirect back if not
    if 'rating' not in request.GET or request.GET['rating'] not in ('1', '-1'):
        return HttpResponseRedirect(snippet.get_absolute_url())
    # Change the existing value of a rating if one is found
    try:
        rating = Rating.objects.get(
            user__pk=request.user.id, snippet__pk=snippet.id)
    except Rating.DoesNotExist:
        rating = Rating(user=request.user, snippet=snippet)
        rating.rating = int(request.GET['rating'])
        rating.save()
        return HttpResponseRedirect(snippet.get_absolute_url())


@login_required
def snippet_flag(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    snippet_flag = SnippetFlag(snippet=snippet, user=request.user)
    form = SnippetFlagForm(data=request.POST, instance=snippet_flag)

    if form.is_valid():
        snippet_flag = form.save()

        admin_link = request.build_absolute_uri(
            reverse('snippet_flag'))

        mail_admins(
            'Snippet flagged: "%s"' % (snippet.title),
            '%s\n\nAdmin link: %s' % (snippet_flag, admin_link),
            fail_silently=True,
        )

        messages.success(request, 'Thank you for helping improve the site!')
    else:
        messages.error(request, 'Invalid form submission')

    return redirect(snippet_detail)

# Docstrings for view functions should always mention the template name that will be used:
# In addition, they should provide a list of variables that are made available to the template.


# def author_snippets(request, username):
#     user = get_object_or_404(User, username=username)
#     snippet_qs = Snippet.objects.filter(author=user)
#     return snippet_list(
#         request,
#         snippet_qs,
#         template_name='cab/user_detail.html',
#         extra_context={'author': user},
#     )

# def search(request):
#     query = request.GET.get('q')
#     snippet_qs = Snippet.objects.none()
#     if query:
#         snippet_qs = Snippet.objects.filter(
#             Q(title__icontains=query) |
#             Q(tags__in=[query]) |
#             Q(author__username__iexact=query)
#         ).distinct().order_by('-rating_score', '-pub_date')

#     return snippet_list(
#         request,
#         queryset=snippet_qs,
#         template_name='search/search.html',
#         extra_context={'query': query},
#     )
