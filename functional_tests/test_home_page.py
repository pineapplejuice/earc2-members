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
		self.assertIn('Emergency Amateur Radio Club', self.browser.title)
		header_text = self.browser.find_element_by_class_name('title').text
		self.assertIn('Emergency Amateur Radio Club', header_text)
	
	def test_log_in(self):
		# Keith goes to home page
		self.browser.get(self.live_server_url)
		
		# He wants to log in, click the login link
		self.browser.find_element_by_link_text('Login').click()
		element = WebDriverWait(self.browser, 10).until(
			EC.presence_of_element_located((By.ID, "id_username")))
		self.assertIn("Member Login", self.browser.find_element_by_id('title').text)
		

		