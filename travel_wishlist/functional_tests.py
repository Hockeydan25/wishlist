import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

    def test_mark_place_as_visited(self):

        self.browser.get(self.live_server_url)  # Load home page
        
        # find visited button. It will have the id visited_pk
        # Where pk = primary key of item. This was configured in the template
        # In this test, mark New York, pk=2 visited
        visited_button = self.browser.find_element_by_id('visited-button-2')
       
        # new_york = self.browser.find_element_by_id('place-name-2')  # find the place name text 

        visited_button.click()  # click button 

        # But now page has to reload. How to get Selenium to wait,
        # And to realize it's a new page, so refresh it's
        # knowledge of the elements on it?
        # Can use an Explicit Wait for a particular condition - in this case, the
        # absence of an element with id = place-name-2

        wait = WebDriverWait(self.browser, 3)
        ny_has_gone = wait.until(EC.invisibility_of_element_located((By.ID, 'place-name-2')))

        # Assert San Francisco is still on page
        self.assertIn('San Francisco', self.browser.page_source)
    
        # But New York is not
        self.assertNotIn('New York', self.browser.page_source)

        # Load visited page
        self.browser.get(self.live_server_url + '/visited')

        # New York should now be on the visited page
        self.assertIn('New York', self.browser.page_source)

        # As well as our other visited places
    
        self.assertIn('Tokyo', self.browser.page_source)
        self.assertIn('Moab', self.browser.page_source)



class PageContentTests(LiveServerTestCase):

    fixtures = ['test_users', 'test_places']

    def setUp(self):
        self.browser = WebDriver  
        self.browser.implicitly_wait(3)
        
        self.browser.get(self.live_server_url + '/admin')   # expect to be redirected to login page 
        self.browser.find_element_by_id('id_username').send_keys('alice')
        self.browser.find_element_by_id('id_password').send_keys('qwertyuiop')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
    

    def tearDown(self):
        self.browser.quit()

    def test_get_home_page_list_of_places(self):

        self.browser.get(self.live_server_url)

        self.assertIn('San Francisco', self.browser.page_source)
        self.assertIn('New York', self.browser.page_source)

        self.assertNotIn('Tokyo', self.browser.page_source)
        self.assertNotIn('Moab', self.browser.page_source)
    

    def test_get_list_of_visited_places(self):

        self.browser.get(self.live_server_url + '/visited')
    
        self.assertIn('Tokyo', self.browser.page_source)
        self.assertIn('Moab', self.browser.page_source)
        
        self.assertNotIn('San Francisco', self.browser.page_source)
        self.assertNotIn('New York', self.browser.page_source)        