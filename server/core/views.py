from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from server.core.serializers import (UserLoginSerializer,
                                     UserRegistrationSerializer)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Validate user credentials, login, and return
        serialized user + auth token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # If the serializer is valid, then the email/password combo is valid.
        # Get the user entity, from which we can get (or create) the auth token
        user = authenticate(**serializer.validated_data)
        if user is None:
            raise ValidationError(
                detail="Incorrect email and password combination. "
                       "Please try again."
            )

        response_data = UserLoginSerializer.login(user, request)
        return Response(response_data)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = ()
    permission_classes = ()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Validate potential new user data, login if successful,
        and return serialized user + auth token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # If the serializer is valid, then the data given is valid.
        # Get the user entity, from the serializer's creation response
        user = self.perform_create(serializer)

        response_data = UserLoginSerializer.login(user, request)
        return Response(response_data, status=status.HTTP_201_CREATED)
