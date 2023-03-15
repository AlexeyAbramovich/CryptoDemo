from django.urls import path
from .views import WelcomePage, Info10CoinsPage, Info250CoinsPage

urlpatterns = [
    path("", WelcomePage.as_view(), name="welcome_page"),
    path("10coins/", Info10CoinsPage.as_view(), name="info_10_coins"),
    path("250coins/", Info250CoinsPage.as_view(), name="info_250_coins")
]
