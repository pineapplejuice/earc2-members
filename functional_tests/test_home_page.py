import time
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


MAX_WAIT = 10

class TestHomePage(FunctionalTest):

    def test_home_page_display(self):
        # Keith goes to home page
        self.browser.get(self.live_server_url)
        
        # He sees the welcome screen to the home page
        self.assertIn('Member Portal', self.browser.title)
        header_text = self.browser.find_element_by_id('title').text
        self.assertIn('Member Portal', header_text)
    
    def test_log_in(self):
        # Keith goes to home page
        self.browser.get(self.live_server_url)
        
        # He wants to log in, click the login link
        self.browser.find_element_by_link_text('Login').click()
        element = WebDriverWait(self.browser, MAX_WAIT).until(
            EC.presence_of_element_located((By.ID, "id_username")))
        self.assertIn("Member Login", self.browser.find_element_by_id('title').text)
        
    def test_new_member_button_from_home_page(self):
        self.browser.get(self.live_server_url)
        
        self.browser.find_element_by_id('new_member_btn').click()
        element = WebDriverWait(self.browser, MAX_WAIT).until(
            EC.title_contains("Membership Application"))
        self.assertIn("Membership Application", self.browser.find_element_by_id('title').text)
    
    def test_login_button_from_home_page(self):
        self.browser.get(self.live_server_url)
       
        self.browser.find_element_by_id('login_btn').click()
        element = WebDriverWait(self.browser, MAX_WAIT).until(
            EC.title_contains("Member Login"))
        self.assertIn("Member Login", self.browser.find_element_by_id('title').text)
    
    def test_member_list_from_home_page(self):
        self.browser.get(self.live_server_url)
       
        self.browser.find_element_by_id('member_list_btn').click()
        element = WebDriverWait(self.browser, MAX_WAIT).until(
            EC.title_contains("Member List"))
        self.assertIn("Member List", self.browser.find_element_by_id('title').text)