from django.contrib import admin
from django.urls import path
from . import  views
urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUS"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("productview/", views.productView, name="Search"),
    path("checkout/", views.checkout, name="Checkout"),
]
