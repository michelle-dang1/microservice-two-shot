from django.urls import path
from shoes_rest.api_views import api_list_shoes, api_show_shoe


urlpatterns = [
    path("shoes/", api_list_shoes, name="api_list_shoes"),
    path("shoes/<int:pk>/", api_show_shoe, name="api_show_shoe"),
]
