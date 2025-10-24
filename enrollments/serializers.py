from rest_framework import serializers
from .models import Enrollment



class EnrollmentSerializer(serializers.ModelSerializer):
    student_email = serializers.ReadOnlyField(source="student.email")
    course_title = serializers.ReadOnlyField(source="course.title")


    class Meta:
        model = Enrollment
        fields = ["id", "student", "student_email", "course", "course_title", "enrolled_at"]
        read_only_fields = ["student", "student_email", "enrolled_at"]