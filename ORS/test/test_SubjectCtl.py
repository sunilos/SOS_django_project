from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.SubjectCtl import SubjectCtl


class TestSubjectCtlRequestToForm(TestCase):
    """Tests for SubjectCtl.request_to_form() — verifies POST data is mapped into self.form."""

    def setUp(self):
        self.ctl = SubjectCtl()

    def test_maps_all_fields(self):
        """All four POST fields must be copied verbatim into self.form."""
        post = {"id": "3", "name": "Physics", "description": "Study of matter", "course_id": "2"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["id"], "3")
        self.assertEqual(self.ctl.form["name"], "Physics")
        self.assertEqual(self.ctl.form["description"], "Study of matter")
        self.assertEqual(self.ctl.form["course_id"], "2")

    def test_missing_fields_use_defaults(self):
        """Missing POST keys must fall back to safe defaults (0 for id, '' for strings)."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["id"], 0)
        self.assertEqual(self.ctl.form["name"], "")
        self.assertEqual(self.ctl.form["description"], "")
        self.assertEqual(self.ctl.form["course_id"], 0)


class TestSubjectCtlModelToForm(TestCase):
    """Tests for SubjectCtl.model_to_form() — verifies a Subject instance is reflected in self.form."""

    def setUp(self):
        self.ctl = SubjectCtl()

    def test_model_to_form_populates_form(self):
        """All Subject attributes must be mapped to the correct form keys."""
        subject = MagicMock()
        subject.id = 5
        subject.subjectName = "Chemistry"
        subject.subjectDescription = "Study of chemicals"
        subject.course_ID = 2
        self.ctl.model_to_form(subject)
        self.assertEqual(self.ctl.form["id"], 5)
        self.assertEqual(self.ctl.form["name"], "Chemistry")
        self.assertEqual(self.ctl.form["description"], "Study of chemicals")
        self.assertEqual(self.ctl.form["course_id"], 2)

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged."""
        original = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original)

    def test_model_to_form_null_course_id_defaults_to_zero(self):
        """When course_ID is falsy, form['course_id'] must be set to 0."""
        subject = MagicMock()
        subject.course_ID = 0
        self.ctl.model_to_form(subject)
        self.assertEqual(self.ctl.form["course_id"], 0)


class TestSubjectCtlFormToModel(TestCase):
    """Tests for SubjectCtl.form_to_model() — verifies form data is written onto a Subject instance."""

    def setUp(self):
        self.ctl = SubjectCtl()

    @patch("ORS.ctl.SubjectCtl.CourseService")
    def test_form_to_model_with_positive_id(self, mock_course_svc):
        """When id > 0, pk must be set and name/description/course_ID mapped onto the model."""
        mock_course_svc.return_value.get.return_value = None
        self.ctl.form.update({"id": "4", "name": "Maths", "description": "Numbers", "course_id": "0"})
        subject = MagicMock()
        result = self.ctl.form_to_model(subject)
        self.assertEqual(subject.id, 4)
        self.assertEqual(subject.subjectName, "Maths")
        self.assertEqual(subject.subjectDescription, "Numbers")
        self.assertIs(result, subject)

    @patch("ORS.ctl.SubjectCtl.CourseService")
    def test_form_to_model_with_zero_id_skips_pk(self, mock_course_svc):
        """When id == 0, obj.id must not be assigned."""
        mock_course_svc.return_value.get.return_value = None
        self.ctl.form.update({"id": "0", "name": "Biology", "description": "Life", "course_id": "0"})
        subject = MagicMock()
        self.ctl.form_to_model(subject)
        set_id_calls = [c for c in subject.mock_calls if "id" in str(c) and "= 0" in str(c)]
        self.assertEqual(len(set_id_calls), 0)

    @patch("ORS.ctl.SubjectCtl.CourseService")
    def test_form_to_model_fetches_course_name(self, mock_course_svc):
        """form_to_model() must look up the course by ID and assign courseName to the model."""
        course = MagicMock()
        course.name = "B.Tech"
        mock_course_svc.return_value.get.return_value = course
        self.ctl.form.update({"id": "0", "name": "Physics", "description": "Waves", "course_id": "3"})
        subject = MagicMock()
        self.ctl.form_to_model(subject)
        self.assertEqual(subject.courseName, "B.Tech")
        self.assertEqual(subject.course_ID, 3)

    @patch("ORS.ctl.SubjectCtl.CourseService")
    def test_form_to_model_no_course_sets_empty_name(self, mock_course_svc):
        """When course_id is 0, courseName must be set to empty string without calling service.get()."""
        mock_course_svc.return_value.get.return_value = None
        self.ctl.form.update({"id": "0", "name": "X", "description": "Y", "course_id": "0"})
        subject = MagicMock()
        self.ctl.form_to_model(subject)
        mock_course_svc.return_value.get.assert_not_called()
        self.assertEqual(subject.courseName, "")


class TestSubjectCtlInputValidation(TestCase):
    """Tests for SubjectCtl.input_validation() — verifies each required-field rule."""

    def setUp(self):
        self.ctl = SubjectCtl()

    def _fill_valid(self):
        self.ctl.form.update({"name": "Physics", "description": "Study of matter", "course_id": "2"})

    def test_valid_form_returns_false(self):
        """A complete valid form must return False (no errors)."""
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())

    def test_missing_name_sets_error(self):
        """An empty name must add 'name' to inputError and return True."""
        self._fill_valid()
        self.ctl.form["name"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("name", self.ctl.form["inputError"])

    def test_missing_description_sets_error(self):
        """An empty description must add 'description' to inputError and return True."""
        self._fill_valid()
        self.ctl.form["description"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("description", self.ctl.form["inputError"])

    def test_missing_course_id_sets_error(self):
        """An empty course_id must add 'course_id' to inputError and return True."""
        self._fill_valid()
        self.ctl.form["course_id"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("course_id", self.ctl.form["inputError"])

    def test_zero_course_id_sets_error(self):
        """course_id == '0' (nothing selected) must add 'course_id' to inputError."""
        self._fill_valid()
        self.ctl.form["course_id"] = "0"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("course_id", self.ctl.form["inputError"])

    def test_all_fields_missing_collects_all_errors(self):
        """When all three fields are absent, all three keys must appear in inputError."""
        self.assertTrue(self.ctl.input_validation())
        for field in ("name", "description", "course_id"):
            self.assertIn(field, self.ctl.form["inputError"])

    def test_error_state_resets_between_calls(self):
        """A second call with valid data must clear inputError and return False."""
        self.ctl.form["name"] = ""
        self.ctl.input_validation()
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())
        self.assertEqual(self.ctl.form["inputError"], {})


class TestSubjectCtlPreload(TestCase):
    """Tests for SubjectCtl.preload() — verifies the course dropdown is built."""

    def setUp(self):
        self.ctl = SubjectCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.CourseService")
    def test_preload_calls_course_search(self, mock_course_svc, mock_html):
        """preload() must call CourseService().search({}) to populate the dropdown."""
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.preload(self.request)
        mock_course_svc.return_value.search.assert_called_once_with({})

    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.CourseService")
    def test_preload_includes_course_select(self, mock_course_svc, mock_html):
        """preload() must include 'course_select' HTML in preload_data."""
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = "<select></select>"
        result = self.ctl.preload(self.request)
        self.assertIn("course_select", result)


class TestSubjectCtlDisplay(TestCase):
    """Tests for SubjectCtl.display() — verifies conditional service call and template render."""

    def setUp(self):
        self.ctl = SubjectCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.CourseService")
    @patch("ORS.ctl.SubjectCtl.render")
    def test_display_with_id_loads_subject(self, mock_render, mock_course_svc, mock_html):
        """display() with id > 0 must call service.get(id) and populate self.form."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        subject = MagicMock()
        subject.id = 2
        subject.subjectName = "Physics"
        subject.subjectDescription = "Waves and energy"
        subject.course_ID = 1
        mock_service = MagicMock()
        mock_service.get.return_value = subject
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 2})

        mock_service.get.assert_called_once_with(2)
        self.assertEqual(self.ctl.form["name"], "Physics")
        self.assertEqual(self.ctl.form["description"], "Waves and energy")

    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.CourseService")
    @patch("ORS.ctl.SubjectCtl.render")
    def test_display_with_zero_id_skips_service(self, mock_render, mock_course_svc, mock_html):
        """display() with id == 0 must not call service.get()."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.get_service = MagicMock()

        self.ctl.display(self.request, params={"id": 0})

        self.ctl.get_service.assert_not_called()

    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.CourseService")
    @patch("ORS.ctl.SubjectCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_course_svc, mock_html):
        """display() must pass 'ors/Subject.html' to render()."""
        mock_render.return_value = MagicMock()
        mock_course_svc.return_value.search.return_value = []
        mock_html.get_list_from_beans.return_value = ""
        self.ctl.display(self.request, params={"id": 0})
        self.assertEqual(mock_render.call_args[0][1], "ors/Subject.html")


class TestSubjectCtlSubmit(TestCase):
    """Tests for SubjectCtl.submit() — verifies duplicate check, save, and re-render."""

    def setUp(self):
        self.ctl = SubjectCtl()
        self.ctl.form.update({"id": "0", "name": "Maths", "description": "Algebra", "course_id": "1"})
        self.request = MagicMock()

    def _mock_service(self, duplicate_exists=False):
        mock_service = MagicMock()
        mock_service.get_model.return_value.objects.filter.return_value.exists.return_value = duplicate_exists
        return mock_service

    @patch("ORS.ctl.SubjectCtl.CourseService")
    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.render")
    @patch("ORS.ctl.SubjectCtl.Subject")
    def test_submit_saves_when_no_duplicate(self, mock_subject_cls, mock_render, mock_html, mock_course_svc):
        """submit() must call service.save() when no duplicate exists."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_course_svc.return_value.get.return_value = None
        subject_instance = MagicMock()
        subject_instance.id = 9
        mock_subject_cls.return_value = subject_instance
        mock_service = self._mock_service(duplicate_exists=False)
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        mock_service.save.assert_called_once_with(subject_instance)

    @patch("ORS.ctl.SubjectCtl.CourseService")
    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.render")
    @patch("ORS.ctl.SubjectCtl.Subject")
    def test_submit_add_sets_success_message(self, mock_subject_cls, mock_render, mock_html, mock_course_svc):
        """submit() with id==0 must set message='Subject added successfully' and error=False."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_course_svc.return_value.get.return_value = None
        mock_subject_cls.return_value = MagicMock()
        mock_service = self._mock_service(duplicate_exists=False)
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        self.assertEqual(self.ctl.form["message"], "Subject added successfully")
        self.assertFalse(self.ctl.form["error"])

    @patch("ORS.ctl.SubjectCtl.CourseService")
    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.render")
    @patch("ORS.ctl.SubjectCtl.Subject")
    def test_submit_update_sets_updated_message(self, mock_subject_cls, mock_render, mock_html, mock_course_svc):
        """submit() with id > 0 must set message='Subject updated successfully'."""
        self.ctl.form["id"] = "5"
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_course_svc.return_value.get.return_value = None
        mock_subject_cls.return_value = MagicMock()
        mock_service = self._mock_service(duplicate_exists=False)
        mock_service.get_model.return_value.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        self.assertEqual(self.ctl.form["message"], "Subject updated successfully")
        self.assertFalse(self.ctl.form["error"])

    @patch("ORS.ctl.SubjectCtl.CourseService")
    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.render")
    def test_submit_sets_error_on_duplicate(self, mock_render, mock_html, mock_course_svc):
        """submit() must set form['error']=True and skip save when a duplicate exists."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_service = self._mock_service(duplicate_exists=True)
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        self.assertTrue(self.ctl.form["error"])
        self.assertIn("already exists", self.ctl.form["message"])
        mock_service.save.assert_not_called()

    @patch("ORS.ctl.SubjectCtl.CourseService")
    @patch("ORS.ctl.SubjectCtl.HtmlUtility")
    @patch("ORS.ctl.SubjectCtl.render")
    @patch("ORS.ctl.SubjectCtl.Subject")
    def test_submit_syncs_subject_id_to_form(self, mock_subject_cls, mock_render, mock_html, mock_course_svc):
        """submit() must copy the DB-assigned subject.id back into form['id']."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_course_svc.return_value.search.return_value = []
        mock_course_svc.return_value.get.return_value = None
        subject_instance = MagicMock()
        subject_instance.id = 42
        mock_subject_cls.return_value = subject_instance
        mock_service = self._mock_service(duplicate_exists=False)
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        self.assertEqual(self.ctl.form["id"], 42)


class TestSubjectCtlMeta(TestCase):
    """Tests for SubjectCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = SubjectCtl()

    def test_get_template_returns_correct_path(self):
        """get_template() must return 'ors/Subject.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Subject.html")

    def test_get_service_returns_subject_service(self):
        """get_service() must return a SubjectService instance."""
        from service.service.SubjectService import SubjectService
        self.assertIsInstance(self.ctl.get_service(), SubjectService)
