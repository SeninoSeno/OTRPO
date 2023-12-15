from django.test import TestCase, LiveServerTestCase, override_settings
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from .models import Fight

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class PokemonsViewTest(TestCase):
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['pokemons'])
        self.assertEqual(len(response.context["pokemons"]), 1292)
        self.assertEqual(response.context["pokemons"][0]["name"], "bulbasaur")

    def test_pokemon(self):
        response = self.client.get(reverse('pokemon', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pokemon"]["name"], "bulbasaur")
        self.assertEqual(response.context["pokemon"]["height"], 7)
        self.assertEqual(response.context["pokemon"]["weight"], 69)
        self.assertEqual(response.context["pokemon"]['stats'][0]['base_stat'], 45)
        self.assertEqual(response.context["pokemon"]['stats'][1]['base_stat'], 49)

    def test_create_fight(self):
        response = self.client.post(reverse('result', args=[1]),
                                            data='{"user_id": 1, "pc_id": 2, '
                                                 '"user_hp": 111, "pc_hp": 222, '
                                                 '"round_count": 99, "winner_id": 1, "email": ""}',
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Fight.objects.all()), 1)
        self.assertEqual(Fight.objects.all()[0].winner_id, 1)
        self.assertEqual(Fight.objects.all()[0].first_pokemon_id, 1)
        self.assertEqual(Fight.objects.all()[0].second_pokemon_id, 2)
        self.assertEqual(Fight.objects.all()[0].first_pokemon_hp, 111)
        self.assertEqual(Fight.objects.all()[0].second_pokemon_hp, 222)
        self.assertEqual(Fight.objects.all()[0].round_count, 99)


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache', }})
class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_index(self):
        self.selenium.get(f"{self.live_server_url}/")
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        self.assertEqual("Pokemoon", self.selenium.title)
        self.assertIn("Рост:", self.selenium.find_element(By.XPATH, "/html/body/div/ol/li[1]/div/p[1]").text)
        self.assertIn("Вес: ", self.selenium.find_element(By.XPATH, "/html/body/div/ol/li[4]/div/p[2]").text)
        self.assertIn("pokeapi.co", self.selenium.find_element(By.XPATH, "/html/body/footer/p").text)

    def test_search(self):
        self.selenium.get(f"{self.live_server_url}/")
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        search_input = self.selenium.find_element(By.ID, "input")
        search_input.send_keys("bul")
        self.selenium.find_element(By.ID, "search").click()
        WebDriverWait(self.selenium, 1000).until(
            lambda driver: driver.find_element(By.XPATH, "/html/body/div/ol/li[1]/div/a[1]")
        )
        self.assertIn("tapu-bulu", self.selenium.find_element(By.XPATH, "/html/body/div/ol/li[4]/div/a[1]").text)

    def test_read(self):
        self.selenium.get(f"{self.live_server_url}/3/info")
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        self.assertEqual("venusaur - информация", self.selenium.title)
        self.assertIn("venusaur", self.selenium.find_element(By.XPATH, "/html/body/header/h1/a[2]").text)
        self.assertIn("82", self.selenium.find_element(By.XPATH, "/html/body/p[5]").text)

    def test_fight(self):
        self.selenium.get(f"{self.live_server_url}/3/fight")
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        self.assertIn("venusaur", self.selenium.title)
        self.assertIn("Вес", self.selenium.find_element(By.XPATH, "/html/body/div/div[2]/p[3]").text)
        self.assertEqual("Атака: 82", self.selenium.find_element(By.XPATH, "/html/body/div/div[1]/p[5]").text)
