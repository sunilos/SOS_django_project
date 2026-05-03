from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import Course
from service.Serializers import CourseSerializers


class CourseCtl(APIView):
    """REST controller for Course CRUD operations."""

    def get(self, request, id=None):
        if id:
            try:
                course = Course.objects.get(id=id)
            except Course.DoesNotExist:
                return Response(
                    {"error": True, "message": "Course not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = CourseSerializers(course)
        else:
            serializer = CourseSerializers(Course.objects.all(), many=True)
        return Response({"error": False, "data": serializer.data})

    def post(self, request):
        serializer = CourseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Course saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id):
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return Response(
                {"error": True, "message": "Course not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CourseSerializers(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Course updated successfully", "data": serializer.data}
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return Response(
                {"error": True, "message": "Course not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        course.delete()
        return Response({"error": False, "message": "Course deleted successfully"})
