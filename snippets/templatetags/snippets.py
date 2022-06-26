from django import template

from snippets.models import Bookmark, Rating, SnippetFlag

register = template.Library()


def do_if_bookmarked(parser, token):
    """ Compilation function for the {% if_bookmarked %} tag
    Usage:
        {% if_bookmarked user snippet %}
    :return: Node class passing two args from the tag and NodeList instance
    """

    # Turns the string into a list of arguments
    bits = token.split_contents()
    # Checks to see if the syntax has the right number of arguments
    if len(bits) != 3:
        # The first item is the name of the tag, not an argument
        raise template.TemplateSyntaxError(
            "%s tag takes two arguments" % bits[0])

    # Pass in the template nodes the parser is expected to look for
    nodelist_true = parser.parse(('else', 'endif_bookmarked'))
    # Checks the first token in the list
    token = parser.next_token()
    if token.contents == 'else':
        # Get the output to display if the snippet wasn't bookmarked
        nodelist_false = parser.parse(('endif_bookmarked',))
        parser.delete_first_token()
    else:
        # Create an empty NodeList and display nothing
        nodelist_false = template.NodeList()
    return IfBookmarkedNode(bits[1], bits[2], nodelist_true, nodelist_false)


class IfBookmarkedNode(template.Node):
    def __init__(self, user, snippet, nodelist_true, nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        # Resolve the variables and returns the actual values
        self.user = template.Variable(user)
        self.snippet = template.Variable(snippet)

    def render(self, context):
        """
        context: a dictionary of variabls available to the template
        :return: string
        """
        # Resolve the variables and return Nothing if it doesn't exist
        try:
            user = self.user.resolve(context)
            snippet = self.snippet.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        # Use the resolved variables to query for an existing bookmark
        if Bookmark.objects.filter(user__pk=user.id, snippet_id=snippet.id):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


register.tag('if_bookmarked', do_if_bookmarked)


def do_if_rated(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError(
            "%s tag takes two arguments" % bits[0])
    nodelist_true = parser.parse(('else', 'endif_rated'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_rated',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfRatedNode(bits[1], bits[2], nodelist_true, nodelist_false)


class IfRatedNode(template.Node):
    def __init__(self, user, snippet, nodelist_true, nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.user = template.Variable(user)
        self.snippet = template.Variable(snippet)

    def render(self, context):
        try:
            user = self.user.resolve(context)
            snippet = self.snippet.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if Rating.objects.filter(user__pk=user.id, snippet__pk=snippet.id):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


register.tag('if_rated', do_if_rated)


def do_get_rating(parser, token):
    bits = token.split_contents()
    # {% get_rating user snippet as rating %}
    if len(bits) != 5:
        raise template.TemplateSyntaxError(
            "%s tag takes four arguments" % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError(
            "Third argument to %s must be 'as'" % bits[0])
    return GetRatingNode(bits[1], bits[2], bits[4])


class GetRatingNode(template.Node):
    def __init__(self, user, snippet, varname):
        self.user = template.Variable(user)
        self.snippet = template.Variable(snippet)
        self.varname = varname

    def render(self, context):
        try:
            user = self.user.resolve(context)
            snippet = self.snippet.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        rating = Rating.objects.get(user__pk=user.id, snippet__pk=snippet.id)
        context[self.varname] = rating
        return ''


register.tag('get_rating', do_get_rating)


# @register.filter
# def has_flagged(user, snippet):
#     if not user.is_authenticated():
#         return False
#     return SnippetFlag.objects.filter(snippet=snippet, user=user).exists()

# A content-retrieving template tag to get the latest snippets
