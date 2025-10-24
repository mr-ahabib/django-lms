from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer
from .permissions import IsStudent

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Student sees only their enrollments
        if user.role == "student":
            return Enrollment.objects.filter(student=user)
        # Instructor/Admin can see all
        return Enrollment.objects.all()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
