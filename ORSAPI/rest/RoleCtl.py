from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import Role
from service.Serializers import RoleSerializers


class RoleCtl(APIView):
    """REST controller for Role CRUD operations."""

    def get(self, request, id=None):
        if id:
            try:
                role = Role.objects.get(id=id)
            except Role.DoesNotExist:
                return Response(
                    {"error": True, "message": "Role not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = RoleSerializers(role)
        else:
            serializer = RoleSerializers(Role.objects.all(), many=True)
        return Response({"error": False, "data": serializer.data})

    def post(self, request):
        serializer = RoleSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Role saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id):
        try:
            role = Role.objects.get(id=id)
        except Role.DoesNotExist:
            return Response(
                {"error": True, "message": "Role not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = RoleSerializers(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Role updated successfully", "data": serializer.data}
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        try:
            role = Role.objects.get(id=id)
        except Role.DoesNotExist:
            return Response(
                {"error": True, "message": "Role not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        role.delete()
        return Response({"error": False, "message": "Role deleted successfully"})
