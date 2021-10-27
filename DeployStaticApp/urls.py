from django.urls import path
from . import views

app_name="nginx_static"

urlpatterns = [
    path('', views.index_view ),
]
