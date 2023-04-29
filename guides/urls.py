from django.urls import path
from .views import *

app_name = "guides"

urlpatterns = [
    path('guides/', HomePageView.as_view(), name="home_url"),
    path('<slug:url_slug>/', BlogView.as_view(), name="blog_url"),
]