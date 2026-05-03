from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import College
from service.Serializers import CollegeSerializers


class CollegeCtl(APIView):
    """REST controller for College CRUD operations."""

    def get(self, request, id=None):
        """Return a single college by id, or all colleges if no id given."""
        if id:
            try:
                college = College.objects.get(id=id)
            except College.DoesNotExist:
                return Response(
                    {"error": True, "message": "College not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = CollegeSerializers(college)
        else:
            colleges = College.objects.all()
            serializer = CollegeSerializers(colleges, many=True)
        return Response({"error": False, "data": serializer.data})

    def post(self, request):
        """Create a new college."""
        serializer = CollegeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "College saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id):
        """Update an existing college."""
        try:
            college = College.objects.get(id=id)
        except College.DoesNotExist:
            return Response(
                {"error": True, "message": "College not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CollegeSerializers(college, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "College updated successfully", "data": serializer.data}
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        """Delete a college by id."""
        try:
            college = College.objects.get(id=id)
        except College.DoesNotExist:
            return Response(
                {"error": True, "message": "College not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        college.delete()
        return Response(
            {"error": False, "message": "College deleted successfully"},
            status=status.HTTP_200_OK,
        )
