""" 
Functionnal tests for 2 user stories :
As Lily I want to make a search about a food directly from the home page.
As Lily i want to login and acces to my account page.
"""


import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from healthier.models import Category, Food_item


class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_script_timeout(10)
        food = Food_item.objects.create(
            open_food_facts_url="https://fr.openfoodfacts.org/produit/3103220009512/chamallows-haribo",
            name="Chamallows",
            nutri_score_fr="d",
            nova_grade=3,
            image_url="https://static.openfoodfacts.org/images/products/310/322/000/9512/front_fr.54.400.jpg",
            id_open_food_facts="1",
            energy_100g="326kcal",
            image_nutrition_url="326kcal",
        )
        food2 = Food_item.objects.create(
            open_food_facts_url="https://fr.openfoodfacts.org/produit/3103220009512/chamallows-haribo",
            name="mallows",
            nutri_score_fr="a",
            nova_grade=2,
            image_url="https://static.openfoodfacts.org/images/products/310/322/000/9512/front_fr.54.400.jpg",
            id_open_food_facts="2",
            energy_100g="326kcal",
            image_nutrition_url="326kcal",
        )
        cat = Category.objects.create(name="bonbons")
        food.categories.add(cat)
        food2.categories.add(cat)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_food_search_from_home_form1(self):
        timeout = 5
        self.selenium.get("%s%s" % (self.live_server_url, "/"))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(By.CLASS_NAME, "modal-footer")
        )
        modal_form = self.selenium.find_element(By.CLASS_NAME, "modal-footer")
        button = modal_form.find_element(By.CLASS_NAME, "btn-primary")
        # workaround to wait until JS fully loaded
        time.sleep(3)
        button.click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(By.ID, "form1")
        )
        search_form = self.selenium.find_element(By.ID, "form1")
        search_box = search_form.find_element(By.CLASS_NAME, "textInput")
        search_box.send_keys("Chamallows" + Keys.ENTER)
        time.sleep(2)
        replacement_item = self.selenium.find_element(By.CLASS_NAME, "space_top")
        self.assertTrue("mallows", replacement_item.text)
        replacement_item.click()
        time.sleep(2)
        self.selenium.find_element(By.TAG_NAME, "h2").click()
        time.sleep(2)
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        time.sleep(3)
        self.assertURLEqual(
            self.selenium.current_url,
            "https://fr.openfoodfacts.org/produit/3103220009512/chamallows-haribo",
        )

    def test_login(self):
        User.objects.create_user(
            "lif65zefus@lkjlkj.eeg",
            email="lif65zefus@lkjlkj.eeg",
            password="123456789",
            first_name="joe",
        )

        self.selenium.get("%s%s" % (self.live_server_url, "/login"))
        time.sleep(3)
        self.selenium.find_element(By.NAME, "login").click()
        time.sleep(1)
        modal_form = self.selenium.find_element(By.ID, "LoginModal")
        button = modal_form.find_element(By.NAME, "Login")
        password = modal_form.find_element(By.NAME, "password")
        username = modal_form.find_element(By.NAME, "username")
        username.send_keys("lif65zefus@lkjlkj.eeg")
        time.sleep(1)
        password.send_keys("123456789")
        time.sleep(1)
        button.click()
        time.sleep(1)
        self.assertURLEqual(
            "/" + self.selenium.current_url.split("/")[3],
            reverse("healthier:myaccount"),
        )
        self.assertTrue(self.selenium.find_element(By.NAME, "user_name").text, "joe")
