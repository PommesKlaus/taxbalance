"""
URLs for the localgaap app:
- Transaction
"""

from django.urls import path
# from localgaap.views import CalculationView
from localgaap.views import SummaryView
from localgaap.views import TransactionCreateView
from localgaap.views import TransactionDetailView

urlpatterns = [
    # path('<int:version_id>/calculation', CalculationView.as_view()),
    path('<int:version_id>/summary', SummaryView.as_view()),
    path('transaction', TransactionCreateView.as_view()),
    path('transaction/<int:pk>', TransactionDetailView.as_view()),
]
