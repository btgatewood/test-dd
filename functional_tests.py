from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_fetch_it_later(self):
        # User goes to the online to-do app's homepage.
        self.browser.get('http://localhost:8000')

        # User notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # User is prompted to enter a task.

        # User enters "buy groceries" into a text box.

        # When the user hits enter, the page updates and displays "1. buy
        # groceries" in a to-do list.

        # A text box prompts the user to add another task.  User enters "cook
        # dinner".

        # The page updates again and displays both tasks in the to-do list.

        # User sees that the site has generated a unique URL to remember the
        # # list.  There is some explanatory text.

        # User visits that URL.  The to-do list is still there.

        # User quits.
        browser.quit()


if __name__ == '__main__':
    unittest.main()
