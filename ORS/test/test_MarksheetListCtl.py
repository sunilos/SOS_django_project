from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.MarksheetListCtl import MarksheetListCtl


class TestMarksheetListCtlPreload(TestCase):
    """Tests for MarksheetListCtl.preload() — verifies student dropdown is built."""

    def setUp(self):
        self.ctl = MarksheetListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.MarksheetListCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetListCtl.StudentService")
    def test_preload_calls_student_search(self, mock_student_svc, mock_html):
        """preload() must call StudentService().search() to load the student list."""
        mock_student_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.preload(self.request)
        mock_student_svc.return_value.search.assert_called_once()

    @patch("ORS.ctl.MarksheetListCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetListCtl.StudentService")
    def test_preload_includes_student_select(self, mock_student_svc, mock_html):
        """preload() must include 'student_select' HTML in preload_data."""
        mock_student_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = "<select></select>"
        result = self.ctl.preload(self.request)
        self.assertIn("student_select", result)


class TestMarksheetListCtlRequestToForm(TestCase):
    """Tests for MarksheetListCtl.request_to_form() — verifies filter fields are mapped."""

    def setUp(self):
        self.ctl = MarksheetListCtl()

    def test_maps_all_filter_fields(self):
        """rollNumber, name, and student_id must be copied into self.form."""
        post = {"rollNumber": "R001", "name": "Raj", "student_id": "3"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["rollNumber"], "R001")
        self.assertEqual(self.ctl.form["student_id"], "3")

    def test_missing_fields_default_to_none(self):
        """Missing filter keys must default to None."""
        self.ctl.request_to_form({})
        self.assertIsNone(self.ctl.form["rollNumber"])
        self.assertIsNone(self.ctl.form["name"])
        self.assertIsNone(self.ctl.form["student_id"])


class TestMarksheetListCtlDisplay(TestCase):
    """Tests for MarksheetListCtl.display() — verifies search and render on GET."""

    def setUp(self):
        self.ctl = MarksheetListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.MarksheetListCtl.StudentService")
    @patch("ORS.ctl.MarksheetListCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetListCtl.render")
    def test_display_calls_search_and_renders(self, mock_render, mock_html, mock_student_svc):
        """display() must call service.search() and pass results as 'pageList'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_student_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = ["ms1"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)
        context = mock_render.call_args[0][2]
        self.assertEqual(context["pageList"], ["ms1"])

    @patch("ORS.ctl.MarksheetListCtl.StudentService")
    @patch("ORS.ctl.MarksheetListCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetListCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_student_svc):
        """display() must render 'ors/MarksheetList.html'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_student_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/MarksheetList.html")


class TestMarksheetListCtlSubmit(TestCase):
    """Tests for MarksheetListCtl.submit() — verifies search-on-POST with form in context."""

    def setUp(self):
        self.ctl = MarksheetListCtl()
        self.request = MagicMock()
        self.request.POST = {"rollNumber": "R002", "name": None, "student_id": None}

    @patch("ORS.ctl.MarksheetListCtl.StudentService")
    @patch("ORS.ctl.MarksheetListCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetListCtl.render")
    def test_submit_populates_form_and_searches(self, mock_render, mock_html, mock_student_svc):
        """submit() must read POST data then call service.search()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_student_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["rollNumber"], "R002")
        mock_service.search.assert_called_once()
        context = mock_render.call_args[0][2]
        self.assertIn("pageList", context)
        self.assertIn("form", context)


class TestMarksheetListCtlMeta(TestCase):
    """Tests for MarksheetListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = MarksheetListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/MarksheetList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/MarksheetList.html")

    def test_get_service_returns_marksheet_service(self):
        """get_service() must return a MarksheetService instance."""
        from service.service.MarksheetService import MarksheetService
        self.assertIsInstance(self.ctl.get_service(), MarksheetService)
