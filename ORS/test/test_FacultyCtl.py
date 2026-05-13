from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.FacultyCtl import FacultyCtl


class TestFacultyCtlRequestToForm(TestCase):
    """Tests for FacultyCtl.request_to_form() — verifies POST data is mapped into self.form."""

    def setUp(self):
        self.ctl = FacultyCtl()

    def test_maps_all_fields(self):
        """All eleven POST fields must be copied verbatim into self.form."""
        post = {
            "id": "2", "firstName": "Anita", "lastName": "Singh",
            "email": "anita@example.com", "mobileNumber": "9876543210",
            "address": "123 MG Road", "gender": "Female", "dob": "1985-07-15",
            "college_ID": "3", "course_ID": "1", "subjectName": "Physics",
        }
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["firstName"], "Anita")
        self.assertEqual(self.ctl.form["email"], "anita@example.com")
        self.assertEqual(self.ctl.form["subjectName"], "Physics")

    def test_missing_fields_use_defaults(self):
        """Missing POST keys must fall back to '' or 0."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["firstName"], "")
        self.assertEqual(self.ctl.form["college_ID"], 0)
        self.assertEqual(self.ctl.form["subjectName"], "")


class TestFacultyCtlModelToForm(TestCase):
    """Tests for FacultyCtl.model_to_form() — verifies a Faculty instance is reflected in self.form."""

    def setUp(self):
        self.ctl = FacultyCtl()

    def test_model_to_form_populates_form(self):
        """All Faculty model attributes must be copied; dob formatted as YYYY-MM-DD."""
        faculty = MagicMock()
        faculty.id = 4
        faculty.firstName = "Anita"
        faculty.lastName = "Singh"
        faculty.email = "anita@example.com"
        faculty.mobileNumber = "9876543210"
        faculty.address = "Addr"
        faculty.gender = "Female"
        faculty.dob.strftime.return_value = "1985-07-15"
        faculty.college_ID = 3
        faculty.course_ID = 1
        faculty.subjectName = "Physics"
        self.ctl.model_to_form(faculty)
        self.assertEqual(self.ctl.form["firstName"], "Anita")
        self.assertEqual(self.ctl.form["subjectName"], "Physics")
        self.assertEqual(self.ctl.form["college_ID"], 3)

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged."""
        original = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original)

    def test_model_to_form_null_dob_uses_empty_string(self):
        """When obj.dob is falsy, form['dob'] must be set to empty string."""
        faculty = MagicMock()
        faculty.dob = None
        faculty.college_ID = 0
        faculty.course_ID = 0
        self.ctl.model_to_form(faculty)
        self.assertEqual(self.ctl.form["dob"], "")


class TestFacultyCtlFormToModel(TestCase):
    """Tests for FacultyCtl.form_to_model() — verifies form data is written onto a Faculty instance."""

    def setUp(self):
        self.ctl = FacultyCtl()

    @patch("ORS.ctl.FacultyCtl.CourseService")
    @patch("ORS.ctl.FacultyCtl.CollegeService")
    def test_form_to_model_with_positive_id(self, mock_college_svc, mock_course_svc):
        """When id > 0, pk must be set and all fields mapped onto the model."""
        mock_college_svc.return_value.get.return_value = None
        mock_course_svc.return_value.get.return_value = None
        self.ctl.form.update({
            "id": "6", "firstName": "Anita", "lastName": "Singh",
            "email": "anita@example.com", "mobileNumber": "9876543210",
            "address": "Addr", "gender": "Female", "dob": "1985-07-15",
            "college_ID": "0", "course_ID": "0", "subjectName": "Physics",
        })
        faculty = MagicMock()
        result = self.ctl.form_to_model(faculty)
        self.assertEqual(faculty.id, 6)
        self.assertEqual(faculty.firstName, "Anita")
        self.assertIs(result, faculty)

    @patch("ORS.ctl.FacultyCtl.CourseService")
    @patch("ORS.ctl.FacultyCtl.CollegeService")
    def test_form_to_model_with_empty_dob_assigns_none(self, mock_college_svc, mock_course_svc):
        """When dob is empty, obj.dob must be set to None."""
        mock_college_svc.return_value.get.return_value = None
        mock_course_svc.return_value.get.return_value = None
        self.ctl.form.update({
            "id": "0", "firstName": "B", "lastName": "C",
            "email": "b@c.com", "mobileNumber": "9000000000",
            "address": "A", "gender": "Male", "dob": "",
            "college_ID": "0", "course_ID": "0", "subjectName": "",
        })
        faculty = MagicMock()
        self.ctl.form_to_model(faculty)
        self.assertIsNone(faculty.dob)

    @patch("ORS.ctl.FacultyCtl.CourseService")
    @patch("ORS.ctl.FacultyCtl.CollegeService")
    def test_form_to_model_fetches_college_and_course_names(self, mock_college_svc, mock_course_svc):
        """form_to_model() must look up college and course names and assign them to the model."""
        college = MagicMock()
        college.name = "MIT"
        course = MagicMock()
        course.name = "B.Tech"
        mock_college_svc.return_value.get.return_value = college
        mock_course_svc.return_value.get.return_value = course
        self.ctl.form.update({
            "id": "0", "firstName": "X", "lastName": "Y",
            "email": "x@y.com", "mobileNumber": "9000000001",
            "address": "A", "gender": "Male", "dob": "",
            "college_ID": "2", "course_ID": "1", "subjectName": "",
        })
        faculty = MagicMock()
        self.ctl.form_to_model(faculty)
        self.assertEqual(faculty.collegeName, "MIT")
        self.assertEqual(faculty.courseName, "B.Tech")


class TestFacultyCtlInputValidation(TestCase):
    """Tests for FacultyCtl.input_validation() — verifies each required-field rule."""

    def setUp(self):
        self.ctl = FacultyCtl()

    def _fill_valid(self):
        self.ctl.form.update({
            "firstName": "Anita", "lastName": "Singh",
            "email": "anita@example.com", "mobileNumber": "9876543210",
            "address": "123 MG Road",
        })

    def test_valid_form_returns_false(self):
        """A complete valid form must return False (no errors)."""
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())

    def test_missing_first_name_sets_error(self):
        """An empty firstName must add 'firstName' to inputError."""
        self._fill_valid()
        self.ctl.form["firstName"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("firstName", self.ctl.form["inputError"])

    def test_missing_last_name_sets_error(self):
        """An empty lastName must add 'lastName' to inputError."""
        self._fill_valid()
        self.ctl.form["lastName"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("lastName", self.ctl.form["inputError"])

    def test_missing_email_sets_error(self):
        """An empty email must add 'email' to inputError."""
        self._fill_valid()
        self.ctl.form["email"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("email", self.ctl.form["inputError"])

    def test_invalid_email_format_sets_error(self):
        """A malformed email must add 'email' to inputError."""
        self._fill_valid()
        self.ctl.form["email"] = "not-an-email"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("email", self.ctl.form["inputError"])

    def test_missing_mobile_sets_error(self):
        """An empty mobileNumber must add 'mobileNumber' to inputError."""
        self._fill_valid()
        self.ctl.form["mobileNumber"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("mobileNumber", self.ctl.form["inputError"])

    def test_invalid_mobile_format_sets_error(self):
        """A non-10-digit mobileNumber must add 'mobileNumber' to inputError."""
        self._fill_valid()
        self.ctl.form["mobileNumber"] = "12345"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("mobileNumber", self.ctl.form["inputError"])

    def test_missing_address_sets_error(self):
        """An empty address must add 'address' to inputError."""
        self._fill_valid()
        self.ctl.form["address"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("address", self.ctl.form["inputError"])

    def test_error_state_resets_between_calls(self):
        """A second call with valid data must clear inputError and return False."""
        self.ctl.form["firstName"] = ""
        self.ctl.input_validation()
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())
        self.assertEqual(self.ctl.form["inputError"], {})


class TestFacultyCtlDisplay(TestCase):
    """Tests for FacultyCtl.display() — verifies conditional service call and template render."""

    def setUp(self):
        self.ctl = FacultyCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.FacultyCtl.CourseService")
    @patch("ORS.ctl.FacultyCtl.CollegeService")
    @patch("ORS.ctl.FacultyCtl.HtmlUtility")
    @patch("ORS.ctl.FacultyCtl.render")
    def test_display_with_id_loads_faculty(self, mock_render, mock_html, mock_college_svc, mock_course_svc):
        """display() with id > 0 must call service.get(id) and populate self.form."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_course_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        faculty = MagicMock()
        faculty.id = 1
        faculty.firstName = "Anita"
        faculty.lastName = "Singh"
        faculty.email = "anita@example.com"
        faculty.mobileNumber = "9876543210"
        faculty.address = "Addr"
        faculty.gender = "Female"
        faculty.dob = None
        faculty.college_ID = 0
        faculty.course_ID = 0
        faculty.subjectName = ""
        mock_service.get.return_value = faculty
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 1})

        mock_service.get.assert_called_once_with(1)
        self.assertEqual(self.ctl.form["firstName"], "Anita")

    @patch("ORS.ctl.FacultyCtl.CourseService")
    @patch("ORS.ctl.FacultyCtl.CollegeService")
    @patch("ORS.ctl.FacultyCtl.HtmlUtility")
    @patch("ORS.ctl.FacultyCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_college_svc, mock_course_svc):
        """display() must pass 'ors/Faculty.html' to render()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_course_svc.return_value.search.return_value = []
        self.ctl.display(self.request, params={"id": 0})
        self.assertEqual(mock_render.call_args[0][1], "ors/Faculty.html")


class TestFacultyCtlSubmit(TestCase):
    """Tests for FacultyCtl.submit() — verifies save, success state, and re-render."""

    def setUp(self):
        self.ctl = FacultyCtl()
        self.ctl.form.update({
            "id": "0", "firstName": "Anita", "lastName": "Singh",
            "email": "anita@example.com", "mobileNumber": "9876543210",
            "address": "Addr", "gender": "Female", "dob": "",
            "college_ID": "0", "course_ID": "0", "subjectName": "Math",
        })
        self.request = MagicMock()

    @patch("ORS.ctl.FacultyCtl.CourseService")
    @patch("ORS.ctl.FacultyCtl.CollegeService")
    @patch("ORS.ctl.FacultyCtl.HtmlUtility")
    @patch("ORS.ctl.FacultyCtl.render")
    @patch("ORS.ctl.FacultyCtl.Faculty")
    def test_submit_calls_service_save(self, mock_faculty_cls, mock_render, mock_html,
                                       mock_college_svc, mock_course_svc):
        """submit() must call service.save() with the Faculty instance built from the form."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_college_svc.return_value.get.return_value = None
        mock_course_svc.return_value.search.return_value = []
        mock_course_svc.return_value.get.return_value = None
        faculty_instance = MagicMock()
        faculty_instance.id = 8
        mock_faculty_cls.return_value = faculty_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.save.assert_called_once_with(faculty_instance)
        self.assertEqual(self.ctl.form["message"], "Data is saved")
        self.assertFalse(self.ctl.form["error"])


class TestFacultyCtlMeta(TestCase):
    """Tests for FacultyCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = FacultyCtl()

    def test_get_template(self):
        """get_template() must return 'ors/Faculty.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Faculty.html")

    def test_get_service_returns_faculty_service(self):
        """get_service() must return a FacultyService instance."""
        from service.service.FacultyService import FacultyService
        self.assertIsInstance(self.ctl.get_service(), FacultyService)
