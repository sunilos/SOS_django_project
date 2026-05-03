from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import Marksheet
from service.Serializers import MarksheetSerializers


class MarksheetCtl(APIView):
    """REST controller for Marksheet CRUD operations."""

    def get(self, request, id=None):
        if id:
            try:
                marksheet = Marksheet.objects.get(id=id)
            except Marksheet.DoesNotExist:
                return Response(
                    {"error": True, "message": "Marksheet not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = MarksheetSerializers(marksheet)
            data = serializer.data
            data["total"] = marksheet.total
            data["percentage"] = marksheet.percentage
        else:
            marksheets = Marksheet.objects.all()
            serializer = MarksheetSerializers(marksheets, many=True)
            data = []
            for obj, item in zip(marksheets, serializer.data):
                entry = dict(item)
                entry["total"] = obj.total
                entry["percentage"] = obj.percentage
                data.append(entry)
        return Response({"error": False, "data": data})

    def post(self, request):
        serializer = MarksheetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Marksheet saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id):
        try:
            marksheet = Marksheet.objects.get(id=id)
        except Marksheet.DoesNotExist:
            return Response(
                {"error": True, "message": "Marksheet not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = MarksheetSerializers(marksheet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "Marksheet updated successfully", "data": serializer.data}
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        try:
            marksheet = Marksheet.objects.get(id=id)
        except Marksheet.DoesNotExist:
            return Response(
                {"error": True, "message": "Marksheet not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        marksheet.delete()
        return Response({"error": False, "message": "Marksheet deleted successfully"})
