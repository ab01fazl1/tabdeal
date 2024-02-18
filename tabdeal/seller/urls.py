from django.urls import path
from .views import TransactionView, AccountView, ChargeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', TransactionView)
router.register(r'accounts', AccountView)
router.register(r'charge', ChargeView)
urlpatterns = router.urls
