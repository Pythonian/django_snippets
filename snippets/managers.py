from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Sum


class SnippetManager(models.Manager):
    """ A manager for the snippet model. """

    def top_authors(self):
        """ Function that returns users with the most number of snippets. """
        return User.objects.annotate(score=Count('snippet')).order_by('-score')

    def most_bookmarked(self):
        """ Function that returns the most bookmarked snippet by users. """
        return self.annotate(score=Count('bookmark')).order_by('-score')

    def top_rated(self):
        """ Function for calculating the top-rated snippets """
        return self.annotate(score=Sum('rating')).order_by('-score')


class LanguageManager(models.Manager):
    def top_languages(self):
        """ Function that returns the top languages by number of snippets. """
        return self.annotate(score=Count('snippet')).order_by('-score')
