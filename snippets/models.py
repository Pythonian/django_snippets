from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse

from markdown import markdown
# http://pygments.org/docs/lexers/
from pygments import formatters, highlight, lexers

from . import managers


class Language(models.Model):
    """ Model to represent the language a code snippet is written.

    name: The name of the language
    slug: A unique slug to identify it in URLs
    language_code: A language code that pygments can use to load
                the appropriate syntax-highlighting module
    file_extension: A file extension to use when offering a snippet in this
                language for download
    mime_type: A MIME type to use when sending a snippet file in this language
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    language_code = models.CharField(max_length=50)
    file_extension = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=100)

    objects = managers.LanguageManager()

    class Meta:
        # Order the languages alphabetically by name
        ordering = ['name']

    def __str__(self):
        """ String representation of a Language. """
        return self.name

    def get_absolute_url(self):
        return reverse('languages:detail', kwargs={'slug': self.slug})

    def get_lexer(self):
        """ Return a lexer (rules) for a particular language. """
        return lexers.get_lexer_by_name(self.language_code)


class Snippet(models.Model):
    """ Model to represent a snippet of code.

    title: The title of the snippet
    language: A foreign key pointing at the Language the snippet is written in.
    author: A foreign key to the User model to represent the snippet’s author.
    description: Store the raw input of the description
    description_html: Store an HTML version of the entered description
    code: The actual code entered by the author
    highlighted_code: A syntax-highlighted HTML version of the original code.
    tags: A list of tags to categorize the snippet
    pub_date: The date and time when the snippet was first posted
    updated_date: The date and time when the snippet was last updated.
    """
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    description_html = models.TextField(editable=False)
    code = models.TextField()
    highlighted_code = models.TextField(editable=False)
    # TODO: Tag field
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = managers.SnippetManager()

    class Meta:
        # Logical ordering of the snippet by descending order
        ordering = ['-pub_date']

    def __str__(self):
        """ String representation of a Snippet. """
        return self.title

    def save(self, *args, **kwargs):
        """
        Line 1 converts the plain-text description to HTML,
        and store that in the description_html field.
        Line 2 does the syntax highlighting, and store the resulting HTML
        in the highlighted_code field.
        """
        self.description_html = markdown(self.description)
        self.highlighted_code = self.highlight()
        super(Snippet, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('snippets:detail', args=[str(self.id)])

    def highlight(self):
        """
        The highlight() function produce the highlighted output. Takes 3 args
            code - The code to highlight
            lexer - The lexer to use
            formatter - The formatter to generate the output
        linenos=True - Generates the output with line numbers
        """
        return highlight(
            self.code, self.language.get_lexer(),
            formatters.HtmlFormatter(linenos=True))

    def get_score(self):
        """
        Calculate a snippet’s total score by summing all ratings attached to it
        """
        return self.rating_set.aggregate(Sum('rating'))


class SnippetFlag(models.Model):
    FLAG_SPAM = 1
    FLAG_INAPPROPRIATE = 2
    FLAG_CHOICES = (
        (FLAG_SPAM, 'Spam'),
        (FLAG_INAPPROPRIATE, 'Inappropriate'),
    )
    snippet = models.ForeignKey(
        Snippet, related_name='flags', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    flag = models.IntegerField(choices=FLAG_CHOICES)

    def __str__(self):
        return '{} flagged as {} by {}'.format(
            self.snippet.title,
            self.get_flag_display(),
            self.user.username,
        )

    def remove_and_ban(self):
        user = self.snippet.author
        user.set_unusable_password()
        user.is_active = False
        user.save()
        self.snippet.delete()


class Bookmark(models.Model):
    """ Model to represent a User's favorite snippets. """
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.snippet} bookmarked by {self.user}"


class Rating(models.Model):
    """ Rating system to mark a snippet useful or not useful. """
    RATING_UP = 1
    RATING_DOWN = -1
    RATING_CHOICES = (
        (RATING_UP, 'useful'),
        (RATING_DOWN, 'not useful'))
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(choices=RATING_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} rating {} ({})".format(self.user,
                                          self.snippet,
                                          self.get_rating_display())
