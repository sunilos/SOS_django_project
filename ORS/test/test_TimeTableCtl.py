from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.TimetableCtl import TimeTableCtl


class TestTimeTableCtlRequestToForm(TestCase):
    """Tests for TimeTableCtl.request_to_form() — verifies POST data is mapped into self.form."""

    def setUp(self):
        self.ctl = TimeTableCtl()

    def test_maps_all_fields(self):
        """All POST fields must be copied into self.form under their snake_case keys."""
        post = {
            "id": "5", "examDate": "2026-06-01", "examTime": "08:00 AM to 11:00 AM",
            "semester": "3", "courseId": "2", "subjectId": "4",
        }
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["id"], "5")
        self.assertEqual(self.ctl.form["exam_date"], "2026-06-01")
        self.assertEqual(self.ctl.form["exam_time"], "08:00 AM to 11:00 AM")
        self.assertEqual(self.ctl.form["semester"], "3")
        self.assertEqual(self.ctl.form["course_id"], "2")
        self.assertEqual(self.ctl.form["subject_id"], "4")

    def test_missing_fields_use_defaults(self):
        """Missing POST keys must fall back to safe defaults."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["id"], 0)
        self.assertEqual(self.ctl.form["exam_date"], "")
        self.assertEqual(self.ctl.form["exam_time"], "")
        self.assertEqual(self.ctl.form["semester"], "")
        self.assertEqual(self.ctl.form["course_id"], 0)
        self.assertEqual(self.ctl.form["subject_id"], 0)

    def test_exam_date_is_stripped(self):
        """examDate must be stripped of leading/trailing whitespace."""
        self.ctl.request_to_form({"examDate": "  2026-06-01  "})
        self.assertEqual(self.ctl.form["exam_date"], "2026-06-01")


class TestTimeTableCtlModelToForm(TestCase):
    """Tests for TimeTableCtl.model_to_form() — verifies a TimeTable instance populates self.form."""

    def setUp(self):
        self.ctl = TimeTableCtl()

    def test_model_to_form_populates_all_fields(self):
        """All model attributes must map to the correct form keys."""
        obj = MagicMock()
        obj.id = 7
        obj.exam_date.strftime.return_value = "2026-06-01"
        obj.exam_time = "08:00 AM to 11:00 AM"
        obj.semester = "3"
        obj.course_id = 2
        obj.subject_id = 4
        self.ctl.model_to_form(obj)
        self.assertEqual(self.ctl.form["id"], 7)
        self.assertEqual(self.ctl.form["exam_time"], "08:00 AM to 11:00 AM")
        self.assertEqual(self.ctl.form["semester"], "3")
        self.assertEqual(self.ctl.form["course_id"], 2)
        self.assertEqual(self.ctl.form["subject_id"], 4)

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged."""
        original = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original)

    def test_model_to_form_null_course_id_defaults_to_zero(self):
        """When course_id is falsy, form['course_id'] must be 0."""
        obj = MagicMock()
        obj.course_id = 0
        obj.subject_id = 0
        self.ctl.model_to_form(obj)
        self.assertEqual(self.ctl.form["course_id"], 0)


class TestTimeTableCtlFormToModel(TestCase):
    """Tests for TimeTableCtl.form_to_model() — verifies form data is written onto a TimeTable instance."""

    def setUp(self):
        self.ctl = TimeTableCtl()

    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    def test_form_to_model_sets_all_fields(self, mock_course_svc, mock_subject_svc):
        """All form fields must be written onto the model object."""
        course = MagicMock()
        course.name = "B.Tech"
        subject = MagicMock()
        subject.name = "Maths"
        mock_course_svc.return_value.get.return_value = course
        mock_subject_svc.return_value.get.return_value = subject

        self.ctl.form.update({
            "id": "3", "exam_date": "2026-06-01", "exam_time": "08:00 AM to 11:00 AM",
            "semester": "2", "course_id": "1", "subject_id": "2",
        })
        obj = MagicMock()
        result = self.ctl.form_to_model(obj)

        self.assertEqual(obj.exam_time, "08:00 AM to 11:00 AM")
        self.assertEqual(obj.semester, "2")
        self.assertEqual(obj.course_id, 1)
        self.assertEqual(obj.course_name, "B.Tech")
        self.assertEqual(obj.subject_id, 2)
        self.assertEqual(obj.subject_name, "Maths")
        self.assertIs(result, obj)

    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    def test_form_to_model_zero_ids_skip_lookup(self, mock_course_svc, mock_subject_svc):
        """When course_id and subject_id are 0, service.get() must not be called."""
        self.ctl.form.update({"id": "0", "exam_date": "", "exam_time": "", "semester": "", "course_id": "0", "subject_id": "0"})
        obj = MagicMock()
        self.ctl.form_to_model(obj)
        mock_course_svc.return_value.get.assert_not_called()
        mock_subject_svc.return_value.get.assert_not_called()
        self.assertEqual(obj.course_name, "")
        self.assertEqual(obj.subject_name, "")


class TestTimeTableCtlInputValidation(TestCase):
    """Tests for TimeTableCtl.input_validation() — verifies each required-field rule."""

    def setUp(self):
        self.ctl = TimeTableCtl()

    def _fill_valid(self):
        self.ctl.form.update({
            "exam_date": "2026-06-01",
            "exam_time": "08:00 AM to 11:00 AM",
            "semester": "3",
            "course_id": "2",
            "subject_id": "4",
        })

    def test_valid_form_returns_false(self):
        """A complete valid form must return False (no errors)."""
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())

    def test_missing_exam_date_sets_error(self):
        """Empty exam_date must add 'exam_date' to inputError and return True."""
        self._fill_valid()
        self.ctl.form["exam_date"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("exam_date", self.ctl.form["inputError"])

    def test_missing_exam_time_sets_error(self):
        """Empty exam_time must add 'exam_time' to inputError."""
        self._fill_valid()
        self.ctl.form["exam_time"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("exam_time", self.ctl.form["inputError"])

    def test_missing_semester_sets_error(self):
        """Empty semester must add 'semester' to inputError."""
        self._fill_valid()
        self.ctl.form["semester"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("semester", self.ctl.form["inputError"])

    def test_zero_course_id_sets_error(self):
        """course_id == '0' must add 'course_id' to inputError."""
        self._fill_valid()
        self.ctl.form["course_id"] = "0"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("course_id", self.ctl.form["inputError"])

    def test_zero_subject_id_sets_error(self):
        """subject_id == '0' must add 'subject_id' to inputError."""
        self._fill_valid()
        self.ctl.form["subject_id"] = "0"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("subject_id", self.ctl.form["inputError"])

    def test_all_fields_missing_collects_all_errors(self):
        """When all five fields are absent, all five keys must appear in inputError."""
        self.assertTrue(self.ctl.input_validation())
        for field in ("exam_date", "exam_time", "semester", "course_id", "subject_id"):
            self.assertIn(field, self.ctl.form["inputError"])

    def test_error_state_resets_between_calls(self):
        """A second call with valid data must clear inputError and return False."""
        self.ctl.input_validation()
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())
        self.assertEqual(self.ctl.form["inputError"], {})


class TestTimeTableCtlPreload(TestCase):
    """Tests for TimeTableCtl.preload() — verifies all four dropdowns are built."""

    def setUp(self):
        self.ctl = TimeTableCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.TimetableCtl.HtmlUtility")
    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    def test_preload_includes_all_selects(self, mock_course_svc, mock_subject_svc, mock_html):
        """preload() must populate exam_time_select, semester_select, course_select, subject_select."""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_html.get_list_from_list.return_value = "<select></select>"
        mock_html.get_list_from_beans.return_value = "<select></select>"
        result = self.ctl.preload(self.request)
        for key in ("exam_time_select", "semester_select", "course_select", "subject_select"):
            self.assertIn(key, result)

    @patch("ORS.ctl.TimetableCtl.HtmlUtility")
    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    def test_preload_calls_course_and_subject_search(self, mock_course_svc, mock_subject_svc, mock_html):
        """preload() must call CourseService().search({}) and SubjectService().search({})."""
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.preload(self.request)
        mock_course_svc.return_value.search.assert_called_once_with({})
        mock_subject_svc.return_value.search.assert_called_once_with({})


class TestTimeTableCtlDisplay(TestCase):
    """Tests for TimeTableCtl.display() — verifies conditional load and render."""

    def setUp(self):
        self.ctl = TimeTableCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.TimetableCtl.HtmlUtility")
    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    @patch("ORS.ctl.TimetableCtl.render")
    def test_display_with_id_loads_timetable(self, mock_render, mock_course_svc, mock_subject_svc, mock_html):
        """display() with id > 0 must call service.get(id) and call model_to_form."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_service = MagicMock()
        timetable = MagicMock()
        timetable.id = 3
        timetable.exam_date.strftime.return_value = "2026-06-01"
        timetable.exam_time = "08:00 AM to 11:00 AM"
        timetable.semester = "2"
        timetable.course_id = 1
        timetable.subject_id = 1
        mock_service.get.return_value = timetable
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 3})

        mock_service.get.assert_called_once_with(3)

    @patch("ORS.ctl.TimetableCtl.HtmlUtility")
    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    @patch("ORS.ctl.TimetableCtl.render")
    def test_display_with_zero_id_skips_service(self, mock_render, mock_course_svc, mock_subject_svc, mock_html):
        """display() with id == 0 must not call service.get()."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.get_service = MagicMock()

        self.ctl.display(self.request, params={"id": 0})

        self.ctl.get_service.assert_not_called()

    @patch("ORS.ctl.TimetableCtl.HtmlUtility")
    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    @patch("ORS.ctl.TimetableCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_course_svc, mock_subject_svc, mock_html):
        """display() must pass 'ors/TimeTable.html' to render()."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.display(self.request, params={"id": 0})
        self.assertEqual(mock_render.call_args[0][1], "ors/TimeTable.html")


class TestTimeTableCtlSubmit(TestCase):
    """Tests for TimeTableCtl.submit() — verifies save, duplicate check, and success state."""

    def setUp(self):
        self.ctl = TimeTableCtl()
        self.ctl.form.update({
            "id": "0", "exam_date": "2026-06-01", "exam_time": "08:00 AM to 11:00 AM",
            "semester": "3", "course_id": "2", "subject_id": "4",
        })
        self.request = MagicMock()

    @patch("ORS.ctl.TimetableCtl.HtmlUtility")
    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    @patch("ORS.ctl.TimetableCtl.render")
    @patch("ORS.ctl.TimetableCtl.TimeTable")
    def test_submit_saves_when_no_duplicate(self, mock_tt_cls, mock_render, mock_course_svc, mock_subject_svc, mock_html):
        """submit() must call service.save() when no duplicate exists."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_course_svc.return_value.get.return_value = None
        mock_subject_svc.return_value.get.return_value = None
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        tt_instance = MagicMock()
        tt_instance.id = 10
        mock_tt_cls.return_value = tt_instance
        mock_service = MagicMock()
        mock_service.get_model.return_value.objects.filter.return_value.exists.return_value = False
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        mock_service.save.assert_called_once()
        self.assertFalse(self.ctl.form["error"])

    @patch("ORS.ctl.TimetableCtl.HtmlUtility")
    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    @patch("ORS.ctl.TimetableCtl.render")
    @patch("ORS.ctl.TimetableCtl.TimeTable")
    def test_submit_sets_error_on_duplicate(self, mock_tt_cls, mock_render, mock_course_svc, mock_subject_svc, mock_html):
        """submit() must set form['error'] = True when a duplicate record exists."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_service = MagicMock()
        mock_service.get_model.return_value.objects.filter.return_value.exists.return_value = True
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        self.assertTrue(self.ctl.form["error"])
        mock_service.save.assert_not_called()

    @patch("ORS.ctl.TimetableCtl.HtmlUtility")
    @patch("ORS.ctl.TimetableCtl.SubjectService")
    @patch("ORS.ctl.TimetableCtl.CourseService")
    @patch("ORS.ctl.TimetableCtl.render")
    @patch("ORS.ctl.TimetableCtl.TimeTable")
    def test_submit_renders_correct_template(self, mock_tt_cls, mock_render, mock_course_svc, mock_subject_svc, mock_html):
        """submit() must render 'ors/TimeTable.html'."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_subject_svc.return_value.search.return_value = []
        mock_course_svc.return_value.get.return_value = None
        mock_subject_svc.return_value.get.return_value = None
        mock_html.get_list_from_list.return_value = ""
        mock_html.get_list_from_beans.return_value = ""
        mock_service = MagicMock()
        mock_service.get_model.return_value.objects.filter.return_value.exists.return_value = False
        mock_tt_cls.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        self.assertEqual(mock_render.call_args[0][1], "ors/TimeTable.html")


class TestTimeTableCtlMeta(TestCase):
    """Tests for TimeTableCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = TimeTableCtl()

    def test_get_template(self):
        """get_template() must return 'ors/TimeTable.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/TimeTable.html")

    def test_get_service_returns_timetable_service(self):
        """get_service() must return a TimeTableService instance."""
        from service.service.TimeTableService import TimeTableService
        self.assertIsInstance(self.ctl.get_service(), TimeTableService)
