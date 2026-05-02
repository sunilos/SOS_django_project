import logging
from abc import ABC, abstractmethod
from django.http import HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


class BaseCtl(ABC):
    """Base class inherited by all application controllers."""

    def __init__(self):
        """Initialize controller attributes with default form values."""
        self.page_list = []
        self.preload_data = {}
        self.form = {
            "id": 0,
            "message": "",
            "error": False,
            "inputError": {},
        }

    def preload(self, request):
        """Load preload data required by the page before rendering."""
        return self.preload_data

    def execute(self, request, params={}):
        """
        Execute method called for each HTTP request.
        Calls display() for GET and submit() for POST after validation.
        """
        logger.info("%s.execute() method=%s params=%s", self.__class__.__name__, request.method, params)

        if "delete" == params.get("action"):
            id: int = params.get("id")
            self.get_service().delete(id)
            logger.info("%s deleted id=%s", self.__class__.__name__, id)

        if "GET" == request.method:
            return self.display(request, params)
        elif "POST" == request.method:
            self.request_to_form(request.POST)
            if self.input_validation():
                logger.warning("%s.input_validation() failed form=%s", self.__class__.__name__, self.form)
                return render(
                    request,
                    self.get_template(),
                    {"form": self.form, "preload_data": self.preload(request)},
                )
            else:
                return self.submit(request, params)
        else:
            logger.error("%s unsupported request method=%s", self.__class__.__name__, request.method)
            message = "Request is not supported"
            return HttpResponse(message)

    @abstractmethod
    def display(self, request, params={}):
        """Display the record for the received ID."""
        pass

    @abstractmethod
    def submit(self, request, params={}):
        """Submit and persist form data."""
        pass

    def request_to_form(self, requestFrom):
        """Populate form values from HTTP POST/GET request data."""
        pass

    def model_to_form(self, obj):
        """Populate form dictionary from a model instance."""
        pass

    def form_to_model(self, obj):
        """Populate a model instance from the form dictionary."""
        pass

    def input_validation(self):
        """Apply input validation and reset error state before each submission."""
        self.form["error"] = False
        self.form["message"] = ""
        self.form["inputError"] = {}  # add this

    @abstractmethod
    def get_template(self):
        """Return the template path for this controller."""
        pass

    @abstractmethod
    def get_service(self):
        """Return the service instance for database operations."""
        pass
