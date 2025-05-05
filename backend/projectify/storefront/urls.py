from django.urls import path
from projectify.storefront.views import (
    contact_us
)

urlpatterns = [
    path('contact-us/', contact_us)
]