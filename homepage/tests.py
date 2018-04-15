from django.test import TestCase

# Create your tests here.
class TestHomePage(TestCase):
	
	def test_render_home_page(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
		