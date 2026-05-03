from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import User
from service.Serializers import UserSerializers


class UserCtl(APIView):
    """REST controller for User CRUD operations."""

    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response(
                    {"error": True, "message": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = UserSerializers(user)
        else:
            serializer = UserSerializers(User.objects.all(), many=True)
        return Response({"error": False, "data": serializer.data})

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "User saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": True, "message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "User updated successfully", "data": serializer.data}
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": True, "message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        user.delete()
        return Response({"error": False, "message": "User deleted successfully"})
