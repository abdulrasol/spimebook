from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from profiles.models import Profile
from profiles.serializer import ProfileSerializer
from profiles.permissions import IsOwnerOrReadOnly


# Create your views here.
class UserProfile(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UsersProfileView(APIView):
    queryset = queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, requset, pk, fromat=None):
        userProfile = Profile.objects.get(pk=pk)
        return Response({})
