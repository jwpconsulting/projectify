from django.urls import path

from projectify.storefront.views import accessibility

urlpatterns = [
    path("accessibility/", accessibility),
]
