import logging
from abc import ABC, abstractmethod
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


class BaseRestCtl(APIView, ABC):
    """Abstract base class inherited by all REST API controllers."""

    @abstractmethod
    def get_model(self):
        """Return the Django model class for this controller."""
        pass

    @abstractmethod
    def get_serializer_class(self):
        """Return the DRF serializer class for this controller."""
        pass

    def get_resource_name(self):
        """Return a display name used in response messages; defaults to the model class name."""
        return self.get_model().__name__

    # --- Response helpers ---

    def ok(self, data):
        """Return 200 OK with a data payload."""
        return Response({"error": False, "data": data})

    def created(self, data, message=None):
        """Return 201 Created; message defaults to '<Resource> saved successfully'."""
        return Response(
            {
                "error": False,
                "message": message or f"{self.get_resource_name()} saved successfully",
                "data": data,
            },
            status=status.HTTP_201_CREATED,
        )

    def updated(self, data, message=None):
        """Return 200 OK after a successful update; message defaults to '<Resource> updated successfully'."""
        return Response(
            {
                "error": False,
                "message": message
                or f"{self.get_resource_name()} updated successfully",
                "data": data,
            },
        )

    def deleted(self, message=None):
        """Return 200 OK after a successful delete; message defaults to '<Resource> deleted successfully'."""
        return Response(
            {
                "error": False,
                "message": message
                or f"{self.get_resource_name()} deleted successfully",
            },
            status=status.HTTP_200_OK,
        )

    def not_found(self, message=None):
        """Return 404 Not Found; message defaults to '<Resource> not found'."""
        return Response(
            {
                "error": True,
                "message": message or f"{self.get_resource_name()} not found",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    def validation_error(self, errors):
        """Return 400 Bad Request with a field-level errors dict."""
        return Response(
            {"error": True, "message": "Validation failed", "errors": errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def bad_request(self, message):
        """Return 400 Bad Request with a plain error message."""
        return Response(
            {"error": True, "message": message},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # --- Default CRUD implementations ---

    def get(self, request, id=None):
        """Return a single record by id, or all records when id is omitted."""
        logger.info("%s.get() id=%s", self.__class__.__name__, id)
        model = self.get_model()
        serializer_class = self.get_serializer_class()
        if id:
            try:
                obj = model.objects.get(id=id)
            except model.DoesNotExist:
                return self.not_found()
            return self.ok(serializer_class(obj).data)
        return self.ok(serializer_class(model.objects.all(), many=True).data)

    def post(self, request):
        """Validate and create a new record; return 201 on success or 400 on validation failure."""
        logger.info("%s.post()", self.__class__.__name__)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.created(serializer.data)
        return self.validation_error(serializer.errors)

    def put(self, request, id):
        """Validate and update an existing record by id; return 404 if not found or 400 on validation failure."""
        logger.info("%s.put() id=%s", self.__class__.__name__, id)
        model = self.get_model()
        try:
            obj = model.objects.get(id=id)
        except model.DoesNotExist:
            return self.not_found()
        serializer = self.get_serializer_class()(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.updated(serializer.data)
        return self.validation_error(serializer.errors)

    def delete(self, request, id):
        """Delete a record by id; return 404 if not found."""
        logger.info("%s.delete() id=%s", self.__class__.__name__, id)
        model = self.get_model()
        try:
            obj = model.objects.get(id=id)
        except model.DoesNotExist:
            return self.not_found()
        obj.delete()
        return self.deleted()
