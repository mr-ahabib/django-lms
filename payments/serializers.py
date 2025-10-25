from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    student_email = serializers.ReadOnlyField(source="student.email")
    course_title = serializers.ReadOnlyField(source="course.title")

    class Meta:
        model = Payment
        fields = ["id", "student", "student_email", "course", "course_title",
                  "enrollment", "amount", "status", "stripe_payment_intent", "created_at"]
        read_only_fields = ["student", "student_email", "status", "stripe_payment_intent", "created_at"]