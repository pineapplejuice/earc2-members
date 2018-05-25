from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10

class TestHomePage(FunctionalTest):

	def test_home_page_display(self):
		# Keith goes to home page
		self.browser.get(self.live_server_url)
		
		# He sees the welcome screen to the home page
		self.assertIn('Emergency Amateur Radio Club', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Welcome', header_text)
		
		# As the membership chair he needs to work on the member list.
		# He sees a link to manage the member list
		self.assertEquals('Manage member list', self.browser.find_element_by_tag_name('a').text)
		