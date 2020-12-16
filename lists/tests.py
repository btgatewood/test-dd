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
    item_text = 'A new list item'

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': self.item_text})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, self.item_text)
    
    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': self.item_text})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-list/')
    
    def test_only_saves_items_on_POST_request(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')
        response = self.client.get('/lists/the-list/')
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
