from rest_framework import viewsets
from .serializers import userSerializers, user_register
from django.contrib.auth.models import User


class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers

class register(viewsets.ModelViewSet):
    serializer_class = userSerializers