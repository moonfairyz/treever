import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from django.urls import reverse

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user.json', 'products.json']
    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def get_url(self, relative_path):
        self.selenium.get('%s%s' % (self.live_server_url, relative_path))
        
    def test_login(self):
        self.get_url('/account/login/')
        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys('user')
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys('user 123')
        
        self.selenium.find_element_by_css_selector(".login").click()
        WebDriverWait(self.selenium, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.get_url('/shop/allproducts/apple-tree/')
        WebDriverWait(self.selenium, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.selenium.find_element_by_css_selector(".cart-add").click()
        time.sleep(10);
