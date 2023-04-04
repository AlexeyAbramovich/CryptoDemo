from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
import requests


class InfoTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        username = 'testuser'
        email = 'testuser@example.com'
        password = 'password'
        self.user = User.objects.create_user(username=username, email=email, password=password)

    def test_coin_gecko_api_response(self):
        path = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&locale=en'
        response = requests.get(path).json()
        self.assertIsNotNone(response)

    def test_welcome_page_exists(self):
        response = self.client.get(reverse("welcome_page"))
        self.assertEqual(response.status_code, 200)

    def test_info_10_coins_page_exists(self):
        response = self.client.get(reverse("info_10_coins"))
        self.assertEqual(response.status_code, 200)

    def test_info_250_coins_page_exists(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse("info_250_coins"))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_user_cant_get_access_to_250_coins_without_authorization(self):
        response = self.client.get(reverse('info_250_coins'))
        self.assertRedirects(response, reverse('welcome_page'))
        self.assertEqual(response.status_code, 302)

    def test_user_cant_get_access_to_10_coins_if_authorized(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('info_10_coins'))
        self.assertRedirects(response, reverse('welcome_page'))
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_search_field(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('info_250_coins'), {'search': 'btc'})
        self.assertEqual(response.context['crypto_info'][0]['name'], 'Bitcoin')
        self.client.logout()

    def test_sorting(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('info_250_coins'), {'sorting': 'total_volume'})
        self.assertEqual(response.context['crypto_info'][0]['name'], 'Tether')
        self.client.logout()

    def tearDown(self):
        self.user.delete()
