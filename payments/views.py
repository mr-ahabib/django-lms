from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
import stripe
import os
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from enrollments.models import Enrollment
from courses.models import Course
from users.models import User

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Student sees only their payments
        if user.role == "student":
            return Payment.objects.filter(student=user)
        # Instructor/Admin sees all payments
        return Payment.objects.all()

    def create(self, request, *args, **kwargs):
        student = request.user
        course_id = request.data.get("course")
        amount = request.data.get("amount")

        # Create Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),  # Stripe expects cents
            currency="usd",
            metadata={"student_id": student.id, "course_id": course_id},
        )

        serializer = self.get_serializer(data={
            "student": student.id,
            "course": course_id,
            "amount": amount,
            "stripe_payment_intent": intent.id,
            "status": "pending"
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "client_secret": intent.client_secret,
            "payment": serializer.data
        }, status=status.HTTP_201_CREATED)


# Webhook for Stripe to notify about payment success
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        student_id = intent["metadata"]["student_id"]
        course_id = intent["metadata"]["course_id"]

        student = User.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        # Update payment status
        payment = Payment.objects.get(stripe_payment_intent=intent["id"])
        payment.status = "paid"
        payment.save()

        # Enroll the student automatically
        Enrollment.objects.create(student=student, course=course)

    return JsonResponse({"status": "success"})
