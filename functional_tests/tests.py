from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time


MAX_WAIT = 2


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assert_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    def await_row_in_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                self.assert_row_in_table(row_text)
                return
            except (AssertionError, WebDriverException) as err:
                if time.time() - start_time > MAX_WAIT:
                    raise err
                time.sleep(0.5)

    def test_can_start_list_for_single_user(self):
        # User goes to the online to-do app's homepage.
        self.browser.get(self.live_server_url)

        # User notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('to-do', header_text)

        # User is prompted to enter a task.
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),
                         'Enter a to-do item')

        # User enters "buy groceries" into a text box.
        input_box.send_keys('buy groceries')

        # When the user hits enter, the page updates and displays "1. buy 
        # groceries" in a to-do list.
        input_box.send_keys(Keys.ENTER)
        self.await_row_in_table('1. buy groceries')

        # A text box prompts the user to add another task.  User enters "cook 
        # dinner".
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('cook dinner')
        input_box.send_keys(Keys.ENTER)

        # The page updates again and displays both tasks in the to-do list.
        self.await_row_in_table('1. buy groceries')
        self.await_row_in_table('2. cook dinner')
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Fred starts a new to-do list.
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('feed the cat')
        input_box.send_keys(Keys.ENTER)
        self.await_row_in_table('1. feed the cat')

        # He notices that his list has a unique URL.
        fred_list_url = self.browser.current_url
        self.assertRegex(fred_list_url, '/lists/.+')

        # A new user, George, comes to the site.
        ## We use a new browser session to make sure that none of Fred's 
        ## information is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # George visits the home page.  There is no sign of Fred's list.
        self.browser.get(self.live_server_url)
        body_text = self.browser.find_element_by_tag_name('body').text
        #self.assertNotIn('buy groceries', body_text)
        #self.assertNotIn('cook dinner', body_text)
        self.assertNotIn('feed the cat', body_text)

        # George starts a new list by entering a new item.
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('read a book')
        input_box.send_keys(Keys.ENTER)
        self.await_row_in_table('1. read a book')

        # George gets his own unique URL.
        george_list_url = self.browser.current_url
        self.assertRegex(george_list_url, '/lists/.+')
        self.assertNotEqual(fred_list_url, george_list_url)

        # There is still no sign of Fred's list.
        body_text = self.browser.get_element_by_tag_name('body').text
        self.assertNotIn('feed the cat', body_text)
