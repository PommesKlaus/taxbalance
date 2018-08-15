"""
URLs for the core app:
- Company
- Version
"""

from django.urls import path
from core.views import CompanyListView, CompanyDetailView, VersionListView, VersionCreateView, VersionDetailView

urlpatterns = [
    path('company', CompanyListView.as_view()),
    path('company/<str:pk>', CompanyDetailView.as_view()),
    path('company/<str:company_id>/versions', VersionListView.as_view()),
    path('version', VersionCreateView.as_view()),
    path('version/<int:pk>', VersionDetailView.as_view()),
]
