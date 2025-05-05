from django.urls import path
from projectify.storefront.views import (
    contact_us,
    accessibility,
    credits,
    ethicalads,
    free_software
)

urlpatterns = [
    path('contact-us/', contact_us),
    path('accessibility/', accessibility),
    path('credits/', credits),
    path('ethicalads/', ethicalads),
    path('free-software/', free_software)
]