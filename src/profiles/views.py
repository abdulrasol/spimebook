from django.shortcuts import render
from rest_framework import generics, permissions
from profiles.models import Profile
from profiles.serializer import ProfileSerializer
from profiles.permissions import IsOwnerOrReadOnly


# Create your views here.
class UserProfile(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
