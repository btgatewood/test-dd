from django.test import TestCase

from lists.models import List, Item


class ListAndItemModelsTest(TestCase):
    def test_saving_items(self):
        list_ = List()
        list_.save()

        item1 = Item()
        item1.text = 'the first item'
        item1.list = list_
        item1.save()

        item2 = Item()
        item2.text = 'a second item'
        item2.list = list_
        item2.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, 'the first item')
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, 'a second item')
        self.assertEqual(saved_items[1].list, list_)


class HomeViewTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_items_only_for_this_list(self):
        this_list = List.objects.create()
        Item.objects.create(text='item 1', list=this_list)
        Item.objects.create(text='item 2', list=this_list)

        that_list = List.objects.create()
        Item.objects.create(text='item 3', list=that_list)
        Item.objects.create(text='item 4', list=that_list)

        response = self.client.get(f'/lists/{this_list.id}/')
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'item 3')
        self.assertNotContains(response, 'item 4')
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    new_item_text = 'a new list item'

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': self.new_item_text})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, self.new_item_text)
    
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', 
                                    data={'item_text': self.new_item_text})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    new_item_text = 'a new list item'

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': self.new_item_text})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, self.new_item_text)
        self.assertEqual(new_item.list, correct_list)
    
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': self.new_item_text})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')