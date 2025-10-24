from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsInstructorOrAdmin



class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=CourseSerializer
    permission_classes=[IsInstructorOrAdmin]



    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)