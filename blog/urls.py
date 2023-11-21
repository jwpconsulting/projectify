"""Blog app urls."""
from django.urls import (
    path,
)

from rest_framework.urlpatterns import (
    format_suffix_patterns,
)

from .views import (
    PostDetailView,
    PostListView,
)

urlpatterns = [
    path("posts/", PostListView.as_view()),
    path("post/<slug:slug>/", PostDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
