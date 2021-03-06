from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed

from .models import Language, Snippet

SITE_NAME = getattr(settings, 'SITE_NAME', None)


class LatestSnippetsFeed(Feed):
    """
    Feed of the most recently published Snippets.
    """
    feed_type = Atom1Feed
    title_template = 'snippets/feeds/title.html'
    description_template = 'snippets/feeds/description.html'
    item_copyright = 'Freely redistributable'
    link = "/snippets/"
    description = "Latest snippets"
    author = "Snippets submitters"

    def title(self):
        if SITE_NAME:
            return f"{SITE_NAME}: Latest snippets"
        else:
            return "Latest snippets"

    def item_author_name(self, item):
        return item.author.username

    def items(self):
        return Snippet.objects.all()[:15]

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date


class SnippetsByAuthorFeed(Feed):
    """
    Feed of the most recent Snippets by a given author.
    """
    feed_type = Atom1Feed
    title_template = 'snippets/feeds/title.html'
    description_template = 'snippets/feeds/description.html'
    item_copyright = 'Freely redistributable'

    def author_name(self, obj):
        return obj.username

    def get_object(self, request, username=None):
        return get_object_or_404(User, username__exact=username)

    def items(self, obj):
        return Snippet.objects.filter(author=obj)[:15]

    def link(self, obj):
        return f"/users/{obj.username}/"

    def title(self, obj):
        if SITE_NAME:
            return f"{SITE_NAME}: Latest snippets posted by {obj.username}"
        else:
            return f"Latest snippets posted by {obj.username}"

    def item_author_name(self, item):
        return item.author.username

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date


class SnippetsByLanguageFeed(Feed):
    """
    Feed of the most recent Snippets in a given language.
    """
    feed_type = Atom1Feed
    title_template = 'snippets/feeds/title.html'
    description_template = 'snippets/feeds/description.html'
    item_copyright = 'Freely redistributable'

    def get_object(self, request, slug=None):
        return get_object_or_404(Language, slug__exact=slug)

    def items(self, obj):
        return Snippet.objects.filter(language=obj)[:15]

    def link(self, obj):
        return obj.get_absolute_url()

    def title(self, obj):
        if SITE_NAME:
            return f"{SITE_NAME}: Latest snippets written in {obj.name}"
        else:
            return f"Latest snippets written in {obj.name}"

    def item_author_name(self, item):
        return item.author.username

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date
