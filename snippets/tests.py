from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from snippets.templatetags.snippets import do_if_bookmarked

from django.contrib.auth.models import User
from snippets.models import Snippet


class IfBookmarkedTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        # create a Snippet with passing the appropriate fields
        self.snippet = Snippet.objects.create(title='test_snippet', language='Python')

    def test_valid_syntax(self):
        # Create a template with the custom filter using valid syntax
        template = Template("{% load snippets %} {% if_bookmarked user snippet %}Bookmarked{% endif_bookmarked %}")
        
        # Create a context with variables for the template to use
        context = Context({"user": self.user, "snippet": self.snippet})
        
        # Render the template with the context
        rendered = template.render(context)
        
        # Assert that the custom filter does not raise a TemplateSyntaxError
        self.assertNotEqual(rendered, "Bookmarked")

    def test_invalid_syntax(self):
        # Create a template with the custom filter using invalid syntax
        template = Template("{% load snippets %} {% if_bookmarked user %}Bookmarked{% endif_bookmarked %}")
        
        # Create a context with a variable for the template to use
        context = Context({"user": self.user})
        
        # Assert that the custom filter raises a TemplateSyntaxError
        with self.assertRaises(TemplateSyntaxError):
            template.render(context)

# Additionally, you can use the assertContains() method to check if the output is as expected, and assertTemplateUsed() method to check if the filter is used.