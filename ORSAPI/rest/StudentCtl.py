from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import Student
from service.Serializers import StudentSerializers


class StudentCtl(APIView):
    """REST controller for Student CRUD operations."""

    def get(self, request, id=None):
        if id:
            try:
                student = Student.objects.get(id=id)
            except Student.DoesNotExist:
                return Response(
                    {"error": True, "message": "Student not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = StudentSerializers(student)
        else:
            serializer = StudentSerializers(Student.objects.all(), many=True)
        return Response({"error": False, "data": serializer.data})

    def post(self, request):
        serializer = StudentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Student saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(
                {"error": True, "message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = StudentSerializers(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Student updated successfully", "data": serializer.data}
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(
                {"error": True, "message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        student.delete()
        return Response({"error": False, "message": "Student deleted successfully"})
