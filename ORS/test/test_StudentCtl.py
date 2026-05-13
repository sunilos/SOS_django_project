from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.StudentCtl import StudentCtl


class TestStudentCtlRequestToForm(TestCase):
    """Tests for StudentCtl.request_to_form() — verifies POST data is mapped into self.form."""

    def setUp(self):
        self.ctl = StudentCtl()

    def test_maps_all_fields(self):
        """All eight POST fields must be copied verbatim into self.form."""
        post = {
            "id": "1", "firstName": "Raj", "lastName": "Kumar",
            "dob": "2000-05-10", "mobileNumber": "9876543210",
            "email": "raj@example.com", "college_ID": "3", "collegeName": "MIT",
        }
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["firstName"], "Raj")
        self.assertEqual(self.ctl.form["email"], "raj@example.com")
        self.assertEqual(self.ctl.form["college_ID"], "3")

    def test_missing_fields_use_defaults(self):
        """Missing POST keys must default to '' or 0."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["firstName"], "")
        self.assertEqual(self.ctl.form["college_ID"], 0)


class TestStudentCtlModelToForm(TestCase):
    """Tests for StudentCtl.model_to_form() — verifies a Student instance populates self.form."""

    def setUp(self):
        self.ctl = StudentCtl()

    def test_model_to_form_populates_form(self):
        """All Student attributes must be copied; dob must be formatted as YYYY-MM-DD."""
        student = MagicMock()
        student.id = 5
        student.firstName = "Raj"
        student.lastName = "Kumar"
        student.dob.strftime.return_value = "2000-05-10"
        student.mobileNumber = "9876543210"
        student.email = "raj@example.com"
        student.college_ID = 3
        student.collegeName = "MIT"

        self.ctl.model_to_form(student)

        self.assertEqual(self.ctl.form["firstName"], "Raj")
        self.assertEqual(self.ctl.form["email"], "raj@example.com")
        self.assertEqual(self.ctl.form["college_ID"], 3)

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged."""
        original = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original)

    def test_model_to_form_with_null_dob_uses_empty_string(self):
        """When obj.dob is falsy, form['dob'] must be set to an empty string."""
        student = MagicMock()
        student.dob = None
        student.college_ID = 0
        self.ctl.model_to_form(student)
        self.assertEqual(self.ctl.form["dob"], "")


class TestStudentCtlFormToModel(TestCase):
    """Tests for StudentCtl.form_to_model() — verifies form data is written onto a Student instance."""

    def setUp(self):
        self.ctl = StudentCtl()

    @patch("ORS.ctl.StudentCtl.CollegeService")
    def test_form_to_model_with_positive_id(self, mock_college_svc):
        """When id > 0, pk must be cast to int and all fields mapped onto the model."""
        mock_college_svc.return_value.get.return_value = None
        self.ctl.form.update({
            "id": "4", "firstName": "Priya", "lastName": "Sharma",
            "dob": "1999-03-22", "mobileNumber": "9111111111",
            "email": "priya@example.com", "college_ID": "0",
        })
        student = MagicMock()
        result = self.ctl.form_to_model(student)
        self.assertEqual(student.id, 4)
        self.assertEqual(student.firstName, "Priya")
        self.assertIs(result, student)

    @patch("ORS.ctl.StudentCtl.CollegeService")
    def test_form_to_model_with_empty_dob_assigns_none(self, mock_college_svc):
        """When dob is empty, obj.dob must be None (not raise an error)."""
        mock_college_svc.return_value.get.return_value = None
        self.ctl.form.update({
            "id": "0", "firstName": "A", "lastName": "B",
            "dob": "", "mobileNumber": "9000000000",
            "email": "a@b.com", "college_ID": "0",
        })
        student = MagicMock()
        self.ctl.form_to_model(student)
        self.assertIsNone(student.dob)


class TestStudentCtlInputValidation(TestCase):
    """Tests for StudentCtl.input_validation() — verifies each required-field rule."""

    def setUp(self):
        self.ctl = StudentCtl()

    def _fill_valid(self):
        self.ctl.form.update({
            "firstName": "Raj", "lastName": "Kumar", "dob": "2000-05-10",
            "mobileNumber": "9876543210", "email": "raj@example.com", "college_ID": "3",
        })

    @patch("ORS.ctl.StudentCtl.CollegeService")
    def test_valid_form_returns_false(self, mock_college_svc):
        """A complete valid form must return False (no errors)."""
        mock_college_svc.return_value.get.return_value = MagicMock(name="MIT")
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

    def test_missing_dob_sets_error(self):
        """An empty dob must add 'dob' to inputError."""
        self._fill_valid()
        self.ctl.form["dob"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("dob", self.ctl.form["inputError"])

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

    def test_missing_college_id_sets_error(self):
        """An empty college_ID must add 'college_ID' to inputError."""
        self._fill_valid()
        self.ctl.form["college_ID"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("college_ID", self.ctl.form["inputError"])

    def test_zero_college_id_sets_error(self):
        """college_ID == '0' must add 'college_ID' to inputError."""
        self._fill_valid()
        self.ctl.form["college_ID"] = "0"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("college_ID", self.ctl.form["inputError"])


class TestStudentCtlGetCollegeName(TestCase):
    """Tests for StudentCtl.get_college_name() — verifies safe lookup by college id."""

    def setUp(self):
        self.ctl = StudentCtl()

    @patch("ORS.ctl.StudentCtl.CollegeService")
    def test_returns_college_name_when_found(self, mock_college_svc):
        """A valid college_id must return the corresponding college name."""
        college = MagicMock()
        college.name = "MIT"
        mock_college_svc.return_value.get.return_value = college
        self.assertEqual(self.ctl.get_college_name("3"), "MIT")

    @patch("ORS.ctl.StudentCtl.CollegeService")
    def test_returns_empty_string_when_not_found(self, mock_college_svc):
        """When get() returns None the method must return an empty string."""
        mock_college_svc.return_value.get.return_value = None
        self.assertEqual(self.ctl.get_college_name("99"), "")

    def test_returns_empty_string_for_null_id(self):
        """A null/empty college_id must return an empty string without calling the service."""
        self.assertEqual(self.ctl.get_college_name(""), "")
        self.assertEqual(self.ctl.get_college_name(None), "")


class TestStudentCtlDisplay(TestCase):
    """Tests for StudentCtl.display() — verifies template rendering and conditional service calls."""

    def setUp(self):
        self.ctl = StudentCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.StudentCtl.CollegeService")
    @patch("ORS.ctl.StudentCtl.HtmlUtility")
    @patch("ORS.ctl.StudentCtl.render")
    def test_display_with_id_loads_student(self, mock_render, mock_html, mock_college_svc):
        """display() with id > 0 must call service.get(id) and populate self.form."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        student = MagicMock()
        student.id = 2
        student.firstName = "Priya"
        student.lastName = "Sharma"
        student.dob = None
        student.mobileNumber = "9000000001"
        student.email = "p@example.com"
        student.college_ID = 0
        student.collegeName = ""
        mock_service.get.return_value = student
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 2})

        mock_service.get.assert_called_once_with(2)
        self.assertEqual(self.ctl.form["firstName"], "Priya")

    @patch("ORS.ctl.StudentCtl.CollegeService")
    @patch("ORS.ctl.StudentCtl.HtmlUtility")
    @patch("ORS.ctl.StudentCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_college_svc):
        """display() must pass 'ors/Student.html' to render()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        self.ctl.display(self.request, params={"id": 0})
        self.assertEqual(mock_render.call_args[0][1], "ors/Student.html")


class TestStudentCtlSubmit(TestCase):
    """Tests for StudentCtl.submit() — verifies save, success state, and re-render."""

    def setUp(self):
        self.ctl = StudentCtl()
        self.ctl.form.update({
            "id": "0", "firstName": "Raj", "lastName": "Kumar",
            "dob": "2000-05-10", "mobileNumber": "9876543210",
            "email": "raj@example.com", "college_ID": "3",
        })
        self.request = MagicMock()

    @patch("ORS.ctl.StudentCtl.CollegeService")
    @patch("ORS.ctl.StudentCtl.HtmlUtility")
    @patch("ORS.ctl.StudentCtl.render")
    @patch("ORS.ctl.StudentCtl.Student")
    def test_submit_calls_service_save(self, mock_student_cls, mock_render, mock_html, mock_college_svc):
        """submit() must call service.save() with the Student instance built from the form."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_college_svc.return_value.get.return_value = None
        student_instance = MagicMock()
        student_instance.id = 10
        student_instance.dob = None
        student_instance.college_ID = 0
        mock_student_cls.return_value = student_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.save.assert_called_once_with(student_instance)

    @patch("ORS.ctl.StudentCtl.CollegeService")
    @patch("ORS.ctl.StudentCtl.HtmlUtility")
    @patch("ORS.ctl.StudentCtl.render")
    @patch("ORS.ctl.StudentCtl.Student")
    def test_submit_sets_success_message(self, mock_student_cls, mock_render, mock_html, mock_college_svc):
        """submit() must set form['message'] = 'Data is saved' and form['error'] = False."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_college_svc.return_value.search.return_value = []
        mock_college_svc.return_value.get.return_value = None
        student_instance = MagicMock()
        student_instance.id = 10
        student_instance.dob = None
        student_instance.college_ID = 0
        mock_student_cls.return_value = student_instance
        self.ctl.get_service = MagicMock(return_value=MagicMock())

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["message"], "Data is saved")
        self.assertFalse(self.ctl.form["error"])


class TestStudentCtlMeta(TestCase):
    """Tests for StudentCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = StudentCtl()

    def test_get_template(self):
        """get_template() must return 'ors/Student.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Student.html")

    def test_get_service_returns_student_service(self):
        """get_service() must return a StudentService instance."""
        from service.service.StudentService import StudentService
        self.assertIsInstance(self.ctl.get_service(), StudentService)
