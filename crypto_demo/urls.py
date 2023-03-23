from django.contrib import admin
from django.urls import path, include
from authorization.views import login_page, signup_page, logout_page

urlpatterns = [
    path('', include("info.urls")),
    path('signup/', signup_page, name="signup"),
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
    path('admin/', admin.site.urls),
]
