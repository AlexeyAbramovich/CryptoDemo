from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from .services.business_logic import get_crypto_data_from_coin_gecko


class WelcomePage(TemplateView):
    template_name = "welcome_page.html"


class Info10CoinsPage(ListView):
    template_name = "info_10_coins_page.html"
    context_object_name = "crypto_info"

    def get_queryset(self):
        return get_crypto_data_from_coin_gecko(False)

# @login_required(login_url='login')
class Info250CoinsPage(ListView):
    template_name = "info_250_coins_page.html"
    context_object_name = "crypto_info"
    paginate_by = 25

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('logout') + '?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_crypto_data_from_coin_gecko(True)
