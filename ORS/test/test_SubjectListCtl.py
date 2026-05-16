from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.SubjectListCtl import SubjectListCtl


class TestSubjectListCtlPreload(TestCase):
    """Tests for SubjectListCtl.preload() — verifies the course dropdown is built."""

    def setUp(self):
        self.ctl = SubjectListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.CourseService")
    def test_preload_calls_course_search(self, mock_course_svc, mock_html):
        """preload() must call CourseService().search({}) to load the course list."""
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.preload(self.request)
        mock_course_svc.return_value.search.assert_called_once_with({})

    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.CourseService")
    def test_preload_includes_course_select(self, mock_course_svc, mock_html):
        """preload() must include 'course_select' HTML in preload_data."""
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = "<select></select>"
        result = self.ctl.preload(self.request)
        self.assertIn("course_select", result)


class TestSubjectListCtlRequestToForm(TestCase):
    """Tests for SubjectListCtl.request_to_form() — verifies filter fields and pagination are mapped."""

    def setUp(self):
        self.ctl = SubjectListCtl()

    def test_maps_all_filter_fields(self):
        """name, description, and course_id must all be copied into self.form."""
        post = {"name": "Physics", "description": "Science", "course_id": "2", "page_number": "1"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["name"], "Physics")
        self.assertEqual(self.ctl.form["description"], "Science")
        self.assertEqual(self.ctl.form["course_id"], "2")

    def test_missing_fields_default_to_none(self):
        """Missing filter keys must default to None so searches are unfiltered."""
        self.ctl.request_to_form({})
        self.assertIsNone(self.ctl.form["name"])
        self.assertIsNone(self.ctl.form["description"])
        self.assertIsNone(self.ctl.form["course_id"])

    def test_reads_page_number_directly(self):
        """page_number from POST must be stored as form['page_number'] unchanged."""
        self.ctl.request_to_form({"page_number": "4"})
        self.assertEqual(self.ctl.form["page_number"], 4)

    def test_page_number_defaults_to_one_when_missing(self):
        """A missing page_number must default to 1."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["page_number"], 1)


class TestSubjectListCtlDisplay(TestCase):
    """Tests for SubjectListCtl.display() — verifies search and render on GET."""

    def setUp(self):
        self.ctl = SubjectListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.SubjectListCtl.CourseService")
    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.render")
    def test_display_calls_search_and_renders(self, mock_render, mock_html, mock_course_svc):
        """display() must call service.search() with page_number=1 and pass results as 'page_list'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = ["s1", "s2"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)
        context = mock_render.call_args[0][2]
        self.assertEqual(context["page_list"], ["s1", "s2"])

    @patch("ORS.ctl.SubjectListCtl.CourseService")
    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.render")
    def test_display_searches_with_page_one(self, mock_render, mock_html, mock_course_svc):
        """display() must call service.search() with page_number=1."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)

    @patch("ORS.ctl.SubjectListCtl.CourseService")
    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_course_svc):
        """display() must render 'ors/SubjectList.html'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/SubjectList.html")

    @patch("ORS.ctl.SubjectListCtl.CourseService")
    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.render")
    def test_display_includes_form_and_preload_in_context(self, mock_render, mock_html, mock_course_svc):
        """display() must include 'form' and 'preload_data' in the template context."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        context = mock_render.call_args[0][2]
        self.assertIn("form", context)
        self.assertIn("preload_data", context)


class TestSubjectListCtlSubmit(TestCase):
    """Tests for SubjectListCtl.submit() — verifies search-on-POST with form in context."""

    def setUp(self):
        self.ctl = SubjectListCtl()
        self.request = MagicMock()
        self.request.POST = {"name": "Chemistry", "description": None, "course_id": None,
                             "page_number": "1"}

    @patch("ORS.ctl.SubjectListCtl.CourseService")
    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.render")
    def test_submit_populates_form_and_searches(self, mock_render, mock_html, mock_course_svc):
        """submit() must read POST data then call service.search()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["name"], "Chemistry")
        mock_service.search.assert_called_once()

    @patch("ORS.ctl.SubjectListCtl.CourseService")
    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.render")
    def test_submit_includes_page_list_and_form_in_context(self, mock_render, mock_html, mock_course_svc):
        """submit() must pass 'page_list', 'form', and 'preload_data' to the template."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.submit(self.request, params={})
        context = mock_render.call_args[0][2]
        self.assertIn("page_list", context)
        self.assertIn("form", context)
        self.assertIn("preload_data", context)

    @patch("ORS.ctl.SubjectListCtl.CourseService")
    @patch("ORS.ctl.SubjectListCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectListCtl.render")
    def test_submit_renders_correct_template(self, mock_render, mock_html, mock_course_svc):
        """submit() must render 'ors/SubjectList.html'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.submit(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/SubjectList.html")


class TestSubjectListCtlMeta(TestCase):
    """Tests for SubjectListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = SubjectListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/SubjectList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/SubjectList.html")

    def test_get_service_returns_subject_service(self):
        """get_service() must return a SubjectService instance."""
        from service.service.SubjectService import SubjectService
        self.assertIsInstance(self.ctl.get_service(), SubjectService)
