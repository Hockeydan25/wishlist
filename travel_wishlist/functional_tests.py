from selenium.webdriver.chrome.webdriver import WebDriver

from django.test import LiveServerTestCase 

from .models import Place

"""
functional testing much slower more realistic, can do things unit testing doesn't like loading page and 
inputting data and clicking buttons checking object positoning and is on the page.
"""

class TitleTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()    # funtion should call to launch chrome manger.
        cls.selenium.implicitly_wait(10)  # waits 10 seconds for loading of page.

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title_shown_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn( 'Travel Wishlist', self.selenium.title)    


class AddPlacesTest(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)  # waits 10 seconds for loading of page.

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_add_new_place(self):

        self.selenium.get(self.live_server_url)
        input_name = self.selenium.find_element_by_id('id_name')  # wishlist html input line puts denver in auto 
        input_name.send_keys('Denver')

        add_button = self.selenium.find_element_by_id('add-new-place')  # wishlist html button id 
        add_button.click()  # auto test will click button to add denver

        denver = self.selenium.find_elemement_by_id('place_name-5')  # wishlist html 
        self.assertEqual('Denver', denver.text)  # checking page object element

        self.assertIn('Denver', self.selenium.page_source)  # text on the page is on visited page 
        self.assertIn('New York', self.selenium.page_source)  # text on the page is on visited page 
        self.assertIn('Tokyo', self.selenium.page_source)  # text on the page is on visited page 

        # this will error if denver, pk=5 isn't there
        denver_db = Place.objects.get(pk=5)
        self.assertEqual('Denver', denver_db.name) 
        self.assertTrue(denver_db.visited)