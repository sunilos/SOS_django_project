from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.TimeTableListCtl import TimeTableListCtl


class TestTimeTableListCtlPreload(TestCase):
    """Tests for TimeTableListCtl.preload() — verifies all four dropdowns are built."""

    def setUp(self):
        self.ctl = TimeTableListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    def test_preload_includes_all_selects(self, mock_course_svc, mock_subject_svc, mock_html):
        """preload() must populate exam_time_select, semester_select, course_select, subject_select."""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_html.get_list_from_list.return_value = "<select></select>"
        mock_html.get_list_from_beans.return_value = "<select></select>"
        result = self.ctl.preload(self.request)
        for key in ("exam_time_select", "semester_select", "course_select", "subject_select"):
            self.assertIn(key, result)

    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    def test_preload_calls_course_and_subject_search(self, mock_course_svc, mock_subject_svc, mock_html):
        """preload() must call CourseService().search({}) and SubjectService().search({})."""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.preload(self.request)
        mock_course_svc.return_value.search.assert_called_once_with({})
        mock_subject_svc.return_value.search.assert_called_once_with({})


class TestTimeTableListCtlRequestToForm(TestCase):
    """Tests for TimeTableListCtl.request_to_form() — verifies filter fields and pagination."""

    def setUp(self):
        self.ctl = TimeTableListCtl()

    def test_maps_all_filter_fields(self):
        """All filter fields must be copied into self.form."""
        post = {
            "examDate": "2026-06-01", "examTime": "08:00 AM to 11:00 AM",
            "semester": "3", "courseId": "2", "subjectId": "4",
            "page_number": "1",
        }
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["exam_date"], "2026-06-01")
        self.assertEqual(self.ctl.form["exam_time"], "08:00 AM to 11:00 AM")
        self.assertEqual(self.ctl.form["semester"], "3")
        self.assertEqual(self.ctl.form["course_id"], "2")
        self.assertEqual(self.ctl.form["subject_id"], "4")

    def test_reads_page_number_directly(self):
        """page_number from POST must be stored as form['page_number'] unchanged."""
        self.ctl.request_to_form({"page_number": "3"})
        self.assertEqual(self.ctl.form["page_number"], 3)

    def test_page_number_defaults_to_one_when_missing(self):
        """A missing page_number must default to 1."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["page_number"], 1)

    def test_missing_fields_default_to_empty(self):
        """Missing filter keys must default to empty string / 0."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["exam_date"], "")
        self.assertEqual(self.ctl.form["exam_time"], "")
        self.assertEqual(self.ctl.form["semester"], "")
        self.assertEqual(self.ctl.form["course_id"], 0)
        self.assertEqual(self.ctl.form["subject_id"], 0)


class TestTimeTableListCtlDisplay(TestCase):
    """Tests for TimeTableListCtl.display() — verifies search on GET and template render."""

    def setUp(self):
        self.ctl = TimeTableListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.render")
    def test_display_calls_search_with_page_one(self, mock_render, mock_html, mock_subject_svc, mock_course_svc):
        """display() must always call service.search() with page_number=1."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = ["t1", "t2"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)

    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.render")
    def test_display_searches_with_page_one(self, mock_render, mock_html, mock_subject_svc, mock_course_svc):
        """display() must not use any page_number from form — always defaults to 1."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)
        self.ctl.form["page_number"] = 5  # should be ignored by display()

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)

    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.render")
    def test_display_passes_page_list_to_context(self, mock_render, mock_html, mock_subject_svc, mock_course_svc):
        """display() must pass 'page_list' in the template context."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = ["t1"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        context = mock_render.call_args[0][2]
        self.assertIn("page_list", context)
        self.assertEqual(context["page_list"], ["t1"])

    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_subject_svc, mock_course_svc):
        """display() must render 'ors/TimeTableList.html'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/TimeTableList.html")


class TestTimeTableListCtlSubmit(TestCase):
    """Tests for TimeTableListCtl.submit() — verifies search-on-POST with correct page."""

    def setUp(self):
        self.ctl = TimeTableListCtl()
        self.request = MagicMock()
        self.request.POST = {
            "examDate": "", "examTime": "", "semester": "",
            "courseId": 0, "subjectId": 0, "page_number": "1",
        }

    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.render")
    def test_submit_reads_post_and_searches(self, mock_render, mock_html, mock_subject_svc, mock_course_svc):
        """submit() must call service.search() after reading POST data."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.search.assert_called_once()

    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.render")
    def test_submit_includes_required_context_keys(self, mock_render, mock_html, mock_subject_svc, mock_course_svc):
        """submit() must pass 'page_list', 'form', and 'preload_data' to the template."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.submit(self.request, params={})
        context = mock_render.call_args[0][2]
        self.assertIn("page_list", context)
        self.assertIn("form", context)
        self.assertIn("preload_data", context)

    @patch("ORS.ctl.TimeTableListCtl.CourseService")
    @patch("ORS.ctl.TimeTableListCtl.SubjectService")
    @patch("ORS.ctl.TimeTableListCtl.HtmlUtility")
    @patch("ORS.ctl.TimeTableListCtl.render")
    def test_submit_renders_correct_template(self, mock_render, mock_html, mock_subject_svc, mock_course_svc):
        """submit() must render 'ors/TimeTableList.html'."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.submit(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/TimeTableList.html")


class TestTimeTableListCtlMeta(TestCase):
    """Tests for TimeTableListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = TimeTableListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/TimeTableList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/TimeTableList.html")

    def test_get_service_returns_timetable_service(self):
        """get_service() must return a TimeTableService instance."""
        from service.service.TimeTableService import TimeTableService
        self.assertIsInstance(self.ctl.get_service(), TimeTableService)
