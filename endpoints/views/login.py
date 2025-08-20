from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email or not password:
            return Response(
                {"detail": "Email or password missing!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Incorrect email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except User.MultipleObjectsReturned:
            return Response(
                {"detail": "Error with provided email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=user_obj.username, password=password)
        if not user:
            return Response(
                {"detail": "Incorrect email or password!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
