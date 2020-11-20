from django.test import TestCase

# Create your tests here.

from lists.models import Item
from lists.views import home


class ItemModelTest(TestCase):
    def test_saving_items(self):
        item1 = Item()
        item1.text = 'the first item'
        item1.save()

        item2 = Item()
        item2.text = 'a second item'
        item2.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(item1.text, saved_items[0].text)
        self.assertEqual(item2.text, saved_items[1].text)


class HomeViewTest(TestCase):    
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
