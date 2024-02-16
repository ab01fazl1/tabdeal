from django.urls import path
from .views import TransactionView, AccountView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'transactions', TransactionView)
router.register(r'accounts', AccountView)

urlpatterns = router.urls

# urlpatterns = [

    # create user -> post seller
    # get user -> get seller

    # seller up balance -> post sellers/me/charge/
    # seller balance -> get sellers/me/balance/
    
    # charging -> post sellers/charge
    # transactions history -> get sellers/me/transactions
# ]