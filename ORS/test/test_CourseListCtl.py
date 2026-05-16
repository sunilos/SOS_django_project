from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.CourseListCtl import CourseListCtl


class TestCourseListCtlRequestToForm(TestCase):
    """Tests for CourseListCtl.request_to_form() — verifies filter fields are mapped."""

    def setUp(self):
        self.ctl = CourseListCtl()

    def test_maps_all_filter_fields(self):
        """name, description, and duration must all be copied into self.form."""
        post = {"name": "B.Tech", "description": "Engineering", "duration": "4 years"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["name"], "B.Tech")
        self.assertEqual(self.ctl.form["description"], "Engineering")
        self.assertEqual(self.ctl.form["duration"], "4 years")

    def test_missing_fields_default_to_none(self):
        """Missing filter keys must default to None so searches are unfiltered."""
        self.ctl.request_to_form({})
        self.assertIsNone(self.ctl.form["name"])
        self.assertIsNone(self.ctl.form["description"])
        self.assertIsNone(self.ctl.form["duration"])


class TestCourseListCtlDisplay(TestCase):
    """Tests for CourseListCtl.display() — verifies search and render on GET."""

    def setUp(self):
        self.ctl = CourseListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.CourseListCtl.render")
    def test_display_calls_search_and_renders(self, mock_render):
        """display() must call service.search() and pass results as 'pageList' to the template."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.search.return_value = ["c1", "c2"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)
        context = mock_render.call_args[0][2]
        self.assertEqual(context["pageList"], ["c1", "c2"])

    @patch("ORS.ctl.CourseListCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must render 'ors/CourseList.html'."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/CourseList.html")


class TestCourseListCtlSubmit(TestCase):
    """Tests for CourseListCtl.submit() — verifies search-on-POST with form in context."""

    def setUp(self):
        self.ctl = CourseListCtl()
        self.request = MagicMock()
        self.request.POST = {"name": "MBA", "description": "Business", "duration": "2 years"}

    @patch("ORS.ctl.CourseListCtl.render")
    def test_submit_populates_form_and_searches(self, mock_render):
        """submit() must read POST data, update self.form, then call service.search()."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["name"], "MBA")
        mock_service.search.assert_called_once()

    @patch("ORS.ctl.CourseListCtl.render")
    def test_submit_includes_form_in_context(self, mock_render):
        """submit() must pass both 'pageList' and 'form' to the template."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.submit(self.request, params={})
        context = mock_render.call_args[0][2]
        self.assertIn("pageList", context)
        self.assertIn("form", context)


class TestCourseListCtlMeta(TestCase):
    """Tests for CourseListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = CourseListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/CourseList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/CourseList.html")

    def test_get_service_returns_course_service(self):
        """get_service() must return a CourseService instance."""
        from service.service.CourseService import CourseService
        self.assertIsInstance(self.ctl.get_service(), CourseService)
