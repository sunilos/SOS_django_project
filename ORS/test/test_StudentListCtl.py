from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.StudentListCtl import StudentListCtl


class TestStudentListCtlPreload(TestCase):
    """Tests for StudentListCtl.preload() — verifies college dropdown is built."""

    def setUp(self):
        self.ctl = StudentListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.StudentListCtl.HtmlUtility")
    @patch("ORS.ctl.StudentListCtl.CollegeService")
    def test_preload_calls_college_search(self, mock_college_svc, mock_html):
        """preload() must call CollegeService().search({}) to load the college list."""
        mock_college_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.preload(self.request)
        mock_college_svc.return_value.search.assert_called_once_with({})

    @patch("ORS.ctl.StudentListCtl.HtmlUtility")
    @patch("ORS.ctl.StudentListCtl.CollegeService")
    def test_preload_includes_college_select(self, mock_college_svc, mock_html):
        """preload() must include 'college_select' HTML in preload_data."""
        mock_college_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = "<select></select>"
        result = self.ctl.preload(self.request)
        self.assertIn("college_select", result)


class TestStudentListCtlRequestToForm(TestCase):
    """Tests for StudentListCtl.request_to_form() — verifies filter fields are mapped."""

    def setUp(self):
        self.ctl = StudentListCtl()

    def test_maps_all_filter_fields(self):
        """All six student search fields must be copied into self.form."""
        post = {"firstName": "Raj", "lastName": "Kumar", "email": "r@e.com",
                "mobileNumber": "9000000000", "dob": "2000-01-01", "college_ID": "3"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["firstName"], "Raj")
        self.assertEqual(self.ctl.form["college_ID"], "3")

    def test_missing_fields_default_to_none(self):
        """Missing filter keys must default to None."""
        self.ctl.request_to_form({})
        for field in ("firstName", "lastName", "email", "mobileNumber", "dob", "college_ID"):
            self.assertIsNone(self.ctl.form[field])


class TestStudentListCtlDisplay(TestCase):
    """Tests for StudentListCtl.display() — verifies search and render on GET."""

    def setUp(self):
        self.ctl = StudentListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.StudentListCtl.CollegeService")
    @patch("ORS.ctl.StudentListCtl.HtmlUtility")
    @patch("ORS.ctl.StudentListCtl.render")
    def test_display_calls_student_search(self, mock_render, mock_html, mock_college_svc):
        """display() must call StudentService.search() and pass results as 'pageList'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = ["s1", "s2"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)
        context = mock_render.call_args[0][2]
        self.assertEqual(context["pageList"], ["s1", "s2"])

    @patch("ORS.ctl.StudentListCtl.CollegeService")
    @patch("ORS.ctl.StudentListCtl.HtmlUtility")
    @patch("ORS.ctl.StudentListCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_college_svc):
        """display() must render 'ors/StudentList.html'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/StudentList.html")


class TestStudentListCtlSubmit(TestCase):
    """Tests for StudentListCtl.submit() — verifies search-on-POST with form in context."""

    def setUp(self):
        self.ctl = StudentListCtl()
        self.request = MagicMock()
        self.request.POST = {"firstName": "Raj", "lastName": "Kumar", "email": None,
                             "mobileNumber": None, "dob": None, "college_ID": None}

    @patch("ORS.ctl.StudentListCtl.CollegeService")
    @patch("ORS.ctl.StudentListCtl.HtmlUtility")
    @patch("ORS.ctl.StudentListCtl.render")
    def test_submit_populates_form_and_searches(self, mock_render, mock_html, mock_college_svc):
        """submit() must populate the form from POST then call StudentService.search()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.search.assert_called_once()
        context = mock_render.call_args[0][2]
        self.assertIn("pageList", context)
        self.assertIn("form", context)


class TestStudentListCtlMeta(TestCase):
    """Tests for StudentListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = StudentListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/StudentList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/StudentList.html")

    def test_get_service_returns_student_service(self):
        """get_service() must return a StudentService instance."""
        from service.service.StudentService import StudentService
        self.assertIsInstance(self.ctl.get_service(), StudentService)
