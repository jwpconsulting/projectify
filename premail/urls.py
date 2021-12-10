"""Premail urlpatterns."""
from django.urls import (
    path,
)

from .views import (
    EmailList,
    EmailPreview,
)


urlpatterns = (
    path(r"email-preview/", EmailList.as_view(), name="email-list"),
    path(
        r"email-preview/<slug:slug>",
        EmailPreview.as_view(),
        name="email-preview",
    ),
)
