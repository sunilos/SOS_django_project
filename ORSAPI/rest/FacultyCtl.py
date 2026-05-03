from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import Faculty
from service.Serializers import FacultySerializers


class FacultyCtl(APIView):
    """REST controller for Faculty CRUD operations."""

    def get(self, request, id=None):
        if id:
            try:
                faculty = Faculty.objects.get(id=id)
            except Faculty.DoesNotExist:
                return Response(
                    {"error": True, "message": "Faculty not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = FacultySerializers(faculty)
        else:
            serializer = FacultySerializers(Faculty.objects.all(), many=True)
        return Response({"error": False, "data": serializer.data})

    def post(self, request):
        serializer = FacultySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Faculty saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id):
        try:
            faculty = Faculty.objects.get(id=id)
        except Faculty.DoesNotExist:
            return Response(
                {"error": True, "message": "Faculty not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = FacultySerializers(faculty, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Faculty updated successfully", "data": serializer.data}
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        try:
            faculty = Faculty.objects.get(id=id)
        except Faculty.DoesNotExist:
            return Response(
                {"error": True, "message": "Faculty not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        faculty.delete()
        return Response({"error": False, "message": "Faculty deleted successfully"})
