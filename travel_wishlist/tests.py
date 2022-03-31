from django.test import TestCase
from django.urls import reverse

from .models import Place
# Create your tests here. reverse extention of python testcase 

class TestHomePage(TestCase):

    def test_home_page_shows_empty_list_message_for_empty_database(self):  # test method when th list is empty 
        home_page_url = reverse('place_list')  # url we are checking for a response
        response = self.client.get(home_page_url)  # 
        self.assertTemplateUsed(response,'travel_wishlist/wishlist.html')  # template that should be used to check
        self.assertContains(response, 'You have no places in your wish list')  # must exact case and characters!
        # djamgo will destroy data in database 