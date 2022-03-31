from urllib import response
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


class TestWishList(TestCase):

    fixtures = ['test_places']  # simialrly this is fixtures is like setup in flask, data we can create test to test agains't

    def test_wishlist_contains_not_visited(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')  # chcks these are in the list
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')  #checks these are not in the list


class VisitedPage(TestCase):

    def test_visited_page_shows_empty_list_message_for_empty_database(self):  # test method when the visited page list is empty 
        response = self.client.get(reverse('places_visited'))  # response name url
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')  # tesing html template
        self.assertContains(response, 'You have not visited any places yet')  # message/text we shouw have  


class VisitedList(TestCase):      
        
    fixtures = ['test_places']  # data we are testing/checking 

    def test_visited_list_shows_visited_places(self):
        response = self.client.get(reverse('places_visited'))  # response name url we want to test
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')  # tesing html template
        self.assertContains(response, 'San Francisco')# chcks these are in the list
        self.assertContains(response, 'Moab')  # spelling important  
        self.assertNotContains(response, 'Tokyo')  #checks these are not in the list
        self.assertNotContains(response, 'New York')

