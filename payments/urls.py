from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PaymentViewSet, stripe_webhook

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = router.urls

# Add webhook endpoint
urlpatterns += [
    path("payments/webhook/", stripe_webhook, name="stripe-webhook"),
]
