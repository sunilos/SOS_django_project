from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.CourseCtl import CourseCtl


class TestCourseCtlRequestToForm(TestCase):
    """Tests for CourseCtl.request_to_form() — verifies POST data is mapped into self.form."""

    def setUp(self):
        self.ctl = CourseCtl()

    def test_request_to_form_all_fields(self):
        """All four POST fields must be copied verbatim into self.form."""
        post = {"id": "2", "name": "B.Tech", "description": "Engineering", "duration": "4 years"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["id"], "2")
        self.assertEqual(self.ctl.form["name"], "B.Tech")
        self.assertEqual(self.ctl.form["description"], "Engineering")
        self.assertEqual(self.ctl.form["duration"], "4 years")

    def test_request_to_form_missing_fields_use_defaults(self):
        """Missing POST keys must fall back to safe defaults."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["id"], 0)
        self.assertEqual(self.ctl.form["name"], "")
        self.assertEqual(self.ctl.form["description"], "")
        self.assertEqual(self.ctl.form["duration"], "")


class TestCourseCtlModelToForm(TestCase):
    """Tests for CourseCtl.model_to_form() — verifies a Course instance is reflected in self.form."""

    def setUp(self):
        self.ctl = CourseCtl()

    def test_model_to_form_populates_form(self):
        """All Course model attributes must be copied into the corresponding form keys."""
        course = MagicMock()
        course.id = 4
        course.name = "MBA"
        course.description = "Business"
        course.duration = "2 years"
        self.ctl.model_to_form(course)
        self.assertEqual(self.ctl.form["id"], 4)
        self.assertEqual(self.ctl.form["name"], "MBA")
        self.assertEqual(self.ctl.form["description"], "Business")
        self.assertEqual(self.ctl.form["duration"], "2 years")

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged."""
        original = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original)


class TestCourseCtlFormToModel(TestCase):
    """Tests for CourseCtl.form_to_model() — verifies form data is written onto a Course instance."""

    def setUp(self):
        self.ctl = CourseCtl()

    def test_form_to_model_with_positive_id(self):
        """When id > 0, pk must be set and all fields mapped onto the model."""
        self.ctl.form.update({"id": "6", "name": "B.Sc", "description": "Science", "duration": "3 years"})
        course = MagicMock()
        result = self.ctl.form_to_model(course)
        self.assertEqual(course.id, 6)
        self.assertEqual(course.name, "B.Sc")
        self.assertEqual(course.description, "Science")
        self.assertEqual(course.duration, "3 years")
        self.assertIs(result, course)

    def test_form_to_model_with_zero_id_skips_pk(self):
        """When id == 0, obj.id must not be assigned."""
        self.ctl.form.update({"id": "0", "name": "Diploma", "description": "Diploma", "duration": "1 year"})
        course = MagicMock()
        self.ctl.form_to_model(course)
        # Verify id=0 was never explicitly set
        set_calls = [c for c in course.mock_calls if "id" in str(c) and "0" in str(c)]
        self.assertEqual(len(set_calls), 0)


class TestCourseCtlInputValidation(TestCase):
    """Tests for CourseCtl.input_validation() — verifies each required-field rule."""

    def setUp(self):
        self.ctl = CourseCtl()

    def _fill_valid(self):
        self.ctl.form.update({"name": "B.Tech", "description": "Engineering", "duration": "4 years"})

    def test_valid_form_returns_false(self):
        """A complete, valid form must return False (no errors)."""
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())

    def test_missing_name_sets_error(self):
        """An empty name must add 'name' to inputError."""
        self._fill_valid()
        self.ctl.form["name"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("name", self.ctl.form["inputError"])

    def test_missing_description_sets_error(self):
        """An empty description must add 'description' to inputError."""
        self._fill_valid()
        self.ctl.form["description"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("description", self.ctl.form["inputError"])

    def test_missing_duration_sets_error(self):
        """An empty duration must add 'duration' to inputError."""
        self._fill_valid()
        self.ctl.form["duration"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("duration", self.ctl.form["inputError"])

    def test_all_fields_missing_collects_all_errors(self):
        """When all three fields are empty all three keys must appear in inputError."""
        self.assertTrue(self.ctl.input_validation())
        for field in ("name", "description", "duration"):
            self.assertIn(field, self.ctl.form["inputError"])

    def test_error_state_resets_between_calls(self):
        """A second call with valid data must clear inputError and return False."""
        self.ctl.form["name"] = ""
        self.ctl.input_validation()
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())
        self.assertEqual(self.ctl.form["inputError"], {})


class TestCourseCtlDisplay(TestCase):
    """Tests for CourseCtl.display() — verifies template rendering and conditional service calls."""

    def setUp(self):
        self.ctl = CourseCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.CourseCtl.render")
    def test_display_with_id_loads_course(self, mock_render):
        """display() with id > 0 must call service.get(id) and populate self.form."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        course = MagicMock()
        course.id = 3
        course.name = "BCA"
        course.description = "Computers"
        course.duration = "3 years"
        mock_service.get.return_value = course
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 3})

        mock_service.get.assert_called_once_with(3)
        self.assertEqual(self.ctl.form["name"], "BCA")

    @patch("ORS.ctl.CourseCtl.render")
    def test_display_with_zero_id_skips_service(self, mock_render):
        """display() with id == 0 must not call the service."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock()
        self.ctl.display(self.request, params={"id": 0})
        self.ctl.get_service.assert_not_called()

    @patch("ORS.ctl.CourseCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must pass 'ors/Course.html' to render()."""
        mock_render.return_value = MagicMock()
        self.ctl.display(self.request, params={"id": 0})
        self.assertEqual(mock_render.call_args[0][1], "ors/Course.html")


class TestCourseCtlSubmit(TestCase):
    """Tests for CourseCtl.submit() — verifies save, success state, and re-render."""

    def setUp(self):
        self.ctl = CourseCtl()
        self.ctl.form.update({"id": "0", "name": "MCA", "description": "CS", "duration": "2 years"})
        self.request = MagicMock()

    @patch("ORS.ctl.CourseCtl.render")
    @patch("ORS.ctl.CourseCtl.Course")
    def test_submit_calls_service_save(self, mock_course_cls, mock_render):
        """submit() must pass the Course instance to service.save()."""
        mock_render.return_value = MagicMock()
        course_instance = MagicMock()
        mock_course_cls.return_value = course_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        mock_service.save.assert_called_once_with(course_instance)

    @patch("ORS.ctl.CourseCtl.render")
    @patch("ORS.ctl.CourseCtl.Course")
    def test_submit_sets_success_message(self, mock_course_cls, mock_render):
        """submit() must set form['message'] = 'Data is saved' and form['error'] = False."""
        mock_render.return_value = MagicMock()
        mock_course_cls.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=MagicMock())

        self.ctl.submit(self.request)

        self.assertEqual(self.ctl.form["message"], "Data is saved")
        self.assertFalse(self.ctl.form["error"])

    @patch("ORS.ctl.CourseCtl.render")
    @patch("ORS.ctl.CourseCtl.Course")
    def test_submit_syncs_course_id_to_form(self, mock_course_cls, mock_render):
        """submit() must copy the DB-assigned course.id back into form['id']."""
        mock_render.return_value = MagicMock()
        course_instance = MagicMock()
        course_instance.id = 77
        mock_course_cls.return_value = course_instance
        self.ctl.get_service = MagicMock(return_value=MagicMock())

        self.ctl.submit(self.request)

        self.assertEqual(self.ctl.form["id"], 77)


class TestCourseCtlMeta(TestCase):
    """Tests for CourseCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = CourseCtl()

    def test_get_template_returns_correct_path(self):
        """get_template() must return 'ors/Course.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Course.html")

    def test_get_service_returns_course_service(self):
        """get_service() must return a CourseService instance."""
        from service.service.CourseService import CourseService
        self.assertIsInstance(self.ctl.get_service(), CourseService)
