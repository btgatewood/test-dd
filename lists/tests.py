from django.test import TestCase

# Create your tests here.

from django.http import HttpRequest
from django.urls import resolve

from lists.views import home


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)
    
    def test_home_page_returns_correct_html(self):
        response = home(HttpRequest())
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do Lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
