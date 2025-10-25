from django.db import models
from django.conf import settings
from courses.models import Course
from enrollments.models import Enrollment

class Payment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email} -> {self.course.title} | {self.status}"
