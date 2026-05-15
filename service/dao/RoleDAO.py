from service.models import Role
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class RoleDAO(BaseDAO):

    def apply_filters(self, q, params):
        """
        Apply filters to the QuerySet based on provided parameters.

        Args:
            q      : initial QuerySet to filter
            params : dict of filter criteria (name, description)

        Returns:
            Filtered QuerySet
        """
        # Filter by name (case-insensitive, partial match)
        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            q = q.filter(name__icontains=val)

        # Filter by description (case-insensitive, partial match)
        val = params.get("description", None)
        if DataValidator.isNotNull(val):
            q = q.filter(description__icontains=val)

        return q

    def get_model(self):
        # Returns the Role model class used by BaseDAO operations
        return Role
