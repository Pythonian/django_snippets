from django.shortcuts import render, get_object_or_404

from ..models import Language


def language_list(request):
    language_list = Language.objects.all()

    template_name = 'languages/list.html'
    context = {'language_list': language_list}

    return render(request, template_name, context)


def language_detail(request, slug):
    language = get_object_or_404(Language, slug=slug)

    template_name = 'languages/detail.html'
    context = {'language': language}

    return render(request, template_name, context)
