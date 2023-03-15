from django.views.generic import ListView, TemplateView
from .services.business_logic import get_crypto_data_from_coin_gecko


class WelcomePage(TemplateView):
    template_name = "welcome_page.html"


class Info10CoinsPage(ListView):
    template_name = "info_10_coins_page.html"
    context_object_name = "crypto_info"

    def get_queryset(self):
        return get_crypto_data_from_coin_gecko(False)


class Info250CoinsPage(ListView):
    template_name = "info_250_coins_page.html"
    context_object_name = "crypto_info"
    paginate_by = 25

    def get_queryset(self):
        return get_crypto_data_from_coin_gecko(True)
