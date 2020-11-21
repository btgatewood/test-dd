from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assert_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_fetch_it_later(self):
        # User goes to the online to-do app's homepage.
        self.browser.get(self.live_server_url)

        # User notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is prompted to enter a task.
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),
                         'Enter a to-do item')

        # User enters "buy groceries" into a text box.
        input_box.send_keys('buy groceries')

        # When the user hits enter, the page updates and displays "1. buy
        # groceries" in a to-do list.
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        self.assert_row_in_table('1. buy groceries')

        # A text box prompts the user to add another task.  User enters "cook
        # dinner".
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('cook dinner')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again and displays both tasks in the to-do list.
        self.assert_row_in_table('1. buy groceries')
        self.assert_row_in_table('2. cook dinner')

        # User sees that the site has generated a unique URL to remember the
        # list.  There is some explanatory text.
        self.fail('Finish the test!')

        # User visits that URL.  The to-do list is still there.

        # User quits.
        browser.quit()
