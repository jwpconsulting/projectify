from django.urls import path
from projectify.storefront.views import (
    contact_us,
    accessibility
)

urlpatterns = [
    path('contact-us/', contact_us),
    path('accessibility', accessibility)
]