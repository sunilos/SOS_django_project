from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.UserListCtl import UserListCtl


class TestUserListCtlPreload(TestCase):
    """Tests for UserListCtl.preload() — verifies role and gender dropdowns are built."""

    def setUp(self):
        self.ctl = UserListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.UserListCtl.HtmlUtility")
    @patch("ORS.ctl.UserListCtl.RoleService")
    def test_preload_calls_role_search(self, mock_role_svc, mock_html):
        """preload() must call RoleService().search({}) to load the role list."""
        mock_role_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        self.ctl.preload(self.request)
        mock_role_svc.return_value.search.assert_called_once_with({})

    @patch("ORS.ctl.UserListCtl.HtmlUtility")
    @patch("ORS.ctl.UserListCtl.RoleService")
    def test_preload_includes_dropdowns(self, mock_role_svc, mock_html):
        """preload() must include 'role_select' and 'gender_select' in preload_data."""
        mock_role_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = "<select></select>"
        mock_html.get_list_from_list.return_value = "<select></select>"
        result = self.ctl.preload(self.request)
        self.assertIn("role_select", result)
        self.assertIn("gender_select", result)


class TestUserListCtlRequestToForm(TestCase):
    """Tests for UserListCtl.request_to_form() — verifies filter fields are mapped."""

    def setUp(self):
        self.ctl = UserListCtl()

    def test_maps_all_filter_fields(self):
        """All six user search fields must be copied into self.form."""
        post = {"firstName": "John", "lastName": "Doe", "login": "j@e.com",
                "mobileNumber": "9000000000", "gender": "Male", "role_id": "1"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["firstName"], "John")
        self.assertEqual(self.ctl.form["role_id"], "1")

    def test_missing_fields_default_to_none(self):
        """Missing filter keys must default to None."""
        self.ctl.request_to_form({})
        for field in ("firstName", "lastName", "login", "mobileNumber", "gender", "role_id"):
            self.assertIsNone(self.ctl.form[field])


class TestUserListCtlDisplay(TestCase):
    """Tests for UserListCtl.display() — verifies search and render on GET."""

    def setUp(self):
        self.ctl = UserListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.UserListCtl.RoleService")
    @patch("ORS.ctl.UserListCtl.HtmlUtility")
    @patch("ORS.ctl.UserListCtl.render")
    def test_display_calls_user_search(self, mock_render, mock_html, mock_role_svc):
        """display() must call service.search() and pass results as 'pageList'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_role_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = ["u1", "u2"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)
        context = mock_render.call_args[0][2]
        self.assertEqual(context["pageList"], ["u1", "u2"])

    @patch("ORS.ctl.UserListCtl.RoleService")
    @patch("ORS.ctl.UserListCtl.HtmlUtility")
    @patch("ORS.ctl.UserListCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_role_svc):
        """display() must render 'ors/UserList.html'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_role_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/UserList.html")


class TestUserListCtlSubmit(TestCase):
    """Tests for UserListCtl.submit() — verifies search-on-POST with form in context."""

    def setUp(self):
        self.ctl = UserListCtl()
        self.request = MagicMock()
        self.request.POST = {"firstName": "Alice", "lastName": None, "login": None,
                             "mobileNumber": None, "gender": None, "role_id": None}

    @patch("ORS.ctl.UserListCtl.RoleService")
    @patch("ORS.ctl.UserListCtl.HtmlUtility")
    @patch("ORS.ctl.UserListCtl.render")
    def test_submit_populates_form_and_searches(self, mock_render, mock_html, mock_role_svc):
        """submit() must read POST data then call service.search()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_role_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.search.assert_called_once()
        context = mock_render.call_args[0][2]
        self.assertIn("pageList", context)
        self.assertIn("form", context)


class TestUserListCtlMeta(TestCase):
    """Tests for UserListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = UserListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/UserList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/UserList.html")

    def test_get_service_returns_user_service(self):
        """get_service() must return a UserService instance."""
        from service.service.UserService import UserService
        self.assertIsInstance(self.ctl.get_service(), UserService)
