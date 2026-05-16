from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.RoleListCtl import RoleListCtl


class TestRoleListCtlRequestToForm(TestCase):
    """Tests for RoleListCtl.request_to_form() — verifies search filter fields are mapped."""

    def setUp(self):
        self.ctl = RoleListCtl()

    def test_request_to_form_maps_all_fields(self):
        """name and description must be copied from the request dict into self.form."""
        post = {"name": "Admin", "description": "Full"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["name"], "Admin")
        self.assertEqual(self.ctl.form["description"], "Full")

    def test_request_to_form_missing_fields_default_to_none(self):
        """Missing search fields must default to None (not empty string) so searches are unfiltered."""
        self.ctl.request_to_form({})
        self.assertIsNone(self.ctl.form["name"])
        self.assertIsNone(self.ctl.form["description"])


class TestRoleListCtlDisplay(TestCase):
    """Tests for RoleListCtl.display() — verifies it searches and renders the list page."""

    def setUp(self):
        self.ctl = RoleListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.RoleListCtl.render")
    def test_display_calls_service_search(self, mock_render):
        """display() must call service.search() with the current form and assign results to page_list."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.search.return_value = ["role1", "role2"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)
        self.assertEqual(self.ctl.page_list, ["role1", "role2"])

    @patch("ORS.ctl.RoleListCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must render 'ors/RoleList.html'."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/RoleList.html")

    @patch("ORS.ctl.RoleListCtl.render")
    def test_display_passes_page_list_in_context(self, mock_render):
        """display() must pass 'pageList' in the template context."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)
        self.ctl.display(self.request, params={})
        context = mock_render.call_args[0][2]
        self.assertIn("pageList", context)


class TestRoleListCtlSubmit(TestCase):
    """Tests for RoleListCtl.submit() — verifies search-on-POST with form in context."""

    def setUp(self):
        self.ctl = RoleListCtl()
        self.request = MagicMock()
        self.request.POST = {"name": "Editor", "description": "Edit"}

    @patch("ORS.ctl.RoleListCtl.render")
    def test_submit_calls_service_search_with_form(self, mock_render):
        """submit() must populate the form from POST then call search() with it."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.search.assert_called_once()
        self.assertEqual(self.ctl.form["name"], "Editor")

    @patch("ORS.ctl.RoleListCtl.render")
    def test_submit_passes_form_in_context(self, mock_render):
        """submit() must include both 'pageList' and 'form' in the template context."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.submit(self.request, params={})
        context = mock_render.call_args[0][2]
        self.assertIn("pageList", context)
        self.assertIn("form", context)


class TestRoleListCtlMeta(TestCase):
    """Tests for RoleListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = RoleListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/RoleList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/RoleList.html")

    def test_get_service_returns_role_service(self):
        """get_service() must return a RoleService instance."""
        from service.service.RoleService import RoleService
        self.assertIsInstance(self.ctl.get_service(), RoleService)
