from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.FacultyListCtl import FacultyListCtl


class TestFacultyListCtlPreload(TestCase):
    """Tests for FacultyListCtl.preload() — verifies college and course dropdowns are built."""

    def setUp(self):
        self.ctl = FacultyListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.FacultyListCtl.HtmlUtility")
    @patch("ORS.ctl.FacultyListCtl.CourseService")
    @patch("ORS.ctl.FacultyListCtl.CollegeService")
    def test_preload_calls_college_and_course_search(self, mock_college_svc, mock_course_svc, mock_html):
        """preload() must call both CollegeService().search({}) and CourseService().search({})."""
        mock_college_svc.return_value.search.return_value = []
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.preload(self.request)
        mock_college_svc.return_value.search.assert_called_once_with({})
        mock_course_svc.return_value.search.assert_called_once_with({})

    @patch("ORS.ctl.FacultyListCtl.HtmlUtility")
    @patch("ORS.ctl.FacultyListCtl.CourseService")
    @patch("ORS.ctl.FacultyListCtl.CollegeService")
    def test_preload_includes_both_selects(self, mock_college_svc, mock_course_svc, mock_html):
        """preload() must include 'college_select' and 'course_select' in preload_data."""
        mock_college_svc.return_value.search.return_value = []
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = "<select></select>"
        result = self.ctl.preload(self.request)
        self.assertIn("college_select", result)
        self.assertIn("course_select", result)


class TestFacultyListCtlRequestToForm(TestCase):
    """Tests for FacultyListCtl.request_to_form() — verifies filter fields are mapped."""

    def setUp(self):
        self.ctl = FacultyListCtl()

    def test_maps_all_filter_fields(self):
        """All five faculty search fields must be copied into self.form."""
        post = {"firstName": "Anita", "lastName": "Singh",
                "email": "anita@example.com", "college_ID": "3", "course_ID": "1"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["firstName"], "Anita")
        self.assertEqual(self.ctl.form["college_ID"], "3")

    def test_missing_fields_default_to_none(self):
        """Missing filter keys must default to None."""
        self.ctl.request_to_form({})
        for field in ("firstName", "lastName", "email", "college_ID", "course_ID"):
            self.assertIsNone(self.ctl.form[field])


class TestFacultyListCtlDisplay(TestCase):
    """Tests for FacultyListCtl.display() — verifies search and render on GET."""

    def setUp(self):
        self.ctl = FacultyListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.FacultyListCtl.CourseService")
    @patch("ORS.ctl.FacultyListCtl.CollegeService")
    @patch("ORS.ctl.FacultyListCtl.HtmlUtility")
    @patch("ORS.ctl.FacultyListCtl.render")
    def test_display_calls_search_and_renders(self, mock_render, mock_html, mock_college_svc, mock_course_svc):
        """display() must call service.search() and pass results as 'pageList'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_course_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = ["f1", "f2"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form)
        context = mock_render.call_args[0][2]
        self.assertEqual(context["pageList"], ["f1", "f2"])

    @patch("ORS.ctl.FacultyListCtl.CourseService")
    @patch("ORS.ctl.FacultyListCtl.CollegeService")
    @patch("ORS.ctl.FacultyListCtl.HtmlUtility")
    @patch("ORS.ctl.FacultyListCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_college_svc, mock_course_svc):
        """display() must render 'ors/FacultyList.html'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_course_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/FacultyList.html")


class TestFacultyListCtlSubmit(TestCase):
    """Tests for FacultyListCtl.submit() — verifies search-on-POST with form in context."""

    def setUp(self):
        self.ctl = FacultyListCtl()
        self.request = MagicMock()
        self.request.POST = {"firstName": "Anita", "lastName": None,
                             "email": None, "college_ID": None, "course_ID": None}

    @patch("ORS.ctl.FacultyListCtl.CourseService")
    @patch("ORS.ctl.FacultyListCtl.CollegeService")
    @patch("ORS.ctl.FacultyListCtl.HtmlUtility")
    @patch("ORS.ctl.FacultyListCtl.render")
    def test_submit_populates_form_and_searches(self, mock_render, mock_html, mock_college_svc, mock_course_svc):
        """submit() must read POST data then call service.search()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_course_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["firstName"], "Anita")
        mock_service.search.assert_called_once()
        context = mock_render.call_args[0][2]
        self.assertIn("pageList", context)
        self.assertIn("form", context)


class TestFacultyListCtlMeta(TestCase):
    """Tests for FacultyListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = FacultyListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/FacultyList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/FacultyList.html")

    def test_get_service_returns_faculty_service(self):
        """get_service() must return a FacultyService instance."""
        from service.service.FacultyService import FacultyService
        self.assertIsInstance(self.ctl.get_service(), FacultyService)
