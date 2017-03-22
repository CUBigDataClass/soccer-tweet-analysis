from django.conf.urls import url, include
from views import get_clubs

urlpatterns = [
    url(r'getclubs/', get_clubs),
]
