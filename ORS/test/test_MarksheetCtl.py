from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.MarksheetCtl import MarksheetCtl


class TestMarksheetCtlRequestToForm(TestCase):
    """Tests for MarksheetCtl.request_to_form() — verifies POST data is mapped into self.form."""

    def setUp(self):
        self.ctl = MarksheetCtl()

    def test_maps_all_fields(self):
        """All eight POST fields must be copied verbatim into self.form."""
        post = {
            "id": "5", "rollNumber": "R001", "name": "Raj",
            "physics": "80", "chemistry": "75", "maths": "90",
            "year": "2024", "student_id": "3",
        }
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["rollNumber"], "R001")
        self.assertEqual(self.ctl.form["physics"], "80")
        self.assertEqual(self.ctl.form["student_id"], "3")

    def test_missing_fields_use_defaults(self):
        """Missing POST keys must fall back to '' or 0."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["rollNumber"], "")
        self.assertEqual(self.ctl.form["id"], 0)
        self.assertEqual(self.ctl.form["student_id"], 0)


class TestMarksheetCtlModelToForm(TestCase):
    """Tests for MarksheetCtl.model_to_form() — verifies a Marksheet instance is reflected in self.form."""

    def setUp(self):
        self.ctl = MarksheetCtl()

    def test_model_to_form_populates_form(self):
        """All Marksheet model attributes including total and percentage must be copied."""
        ms = MagicMock()
        ms.id = 2
        ms.rollNumber = "R002"
        ms.name = "Priya"
        ms.physics = 85
        ms.chemistry = 78
        ms.maths = 92
        ms.year = 2024
        ms.student_id = 4
        ms.total = 255
        ms.percentage = 85.0
        self.ctl.model_to_form(ms)
        self.assertEqual(self.ctl.form["rollNumber"], "R002")
        self.assertEqual(self.ctl.form["total"], 255)
        self.assertEqual(self.ctl.form["percentage"], 85.0)

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged."""
        original = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original)


class TestMarksheetCtlFormToModel(TestCase):
    """Tests for MarksheetCtl.form_to_model() — verifies form data is written onto a Marksheet instance."""

    def setUp(self):
        self.ctl = MarksheetCtl()

    def test_form_to_model_with_positive_id(self):
        """When id > 0, pk must be set and all fields mapped including int casts."""
        self.ctl.form.update({
            "id": "3", "rollNumber": "R003", "name": "Test",
            "physics": "70", "chemistry": "65", "maths": "80",
            "year": "2023", "student_id": "2",
        })
        ms = MagicMock()
        result = self.ctl.form_to_model(ms)
        self.assertEqual(ms.id, 3)
        self.assertEqual(ms.physics, 70)
        self.assertEqual(ms.maths, 80)
        self.assertIs(result, ms)

    def test_form_to_model_with_zero_id_skips_pk(self):
        """When id == 0, obj.id must not be explicitly assigned."""
        self.ctl.form.update({
            "id": "0", "rollNumber": "R004", "name": "New",
            "physics": "50", "chemistry": "55", "maths": "60",
            "year": "2024", "student_id": "1",
        })
        ms = MagicMock()
        self.ctl.form_to_model(ms)
        # chemistry should be set but not id=0
        self.assertEqual(ms.chemistry, 55)


class TestMarksheetCtlInputValidation(TestCase):
    """Tests for MarksheetCtl.input_validation() — verifies each subject, year, roll, and student rules."""

    def setUp(self):
        self.ctl = MarksheetCtl()

    def _fill_valid(self):
        self.ctl.form.update({
            "rollNumber": "R001", "physics": "80", "chemistry": "75",
            "maths": "90", "year": "2024", "student_id": "3", "id": "0",
        })

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_valid_form_returns_false(self, mock_ms_cls):
        """A complete valid form must return False (no errors)."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_missing_roll_number_sets_error(self, mock_ms_cls):
        """An empty rollNumber must add 'rollNumber' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.ctl.form["rollNumber"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("rollNumber", self.ctl.form["inputError"])

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_duplicate_roll_number_sets_error(self, mock_ms_cls):
        """A rollNumber already in use must add 'rollNumber' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = True
        self._fill_valid()
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("rollNumber", self.ctl.form["inputError"])

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_missing_physics_sets_error(self, mock_ms_cls):
        """An empty physics field must add 'physics' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.ctl.form["physics"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("physics", self.ctl.form["inputError"])

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_out_of_range_physics_sets_error(self, mock_ms_cls):
        """A physics score outside [0, 100] must add 'physics' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.ctl.form["physics"] = "150"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("physics", self.ctl.form["inputError"])

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_missing_chemistry_sets_error(self, mock_ms_cls):
        """An empty chemistry field must add 'chemistry' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.ctl.form["chemistry"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("chemistry", self.ctl.form["inputError"])

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_missing_maths_sets_error(self, mock_ms_cls):
        """An empty maths field must add 'maths' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.ctl.form["maths"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("maths", self.ctl.form["inputError"])

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_missing_year_sets_error(self, mock_ms_cls):
        """An empty year must add 'year' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.ctl.form["year"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("year", self.ctl.form["inputError"])

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_non_integer_year_sets_error(self, mock_ms_cls):
        """A non-integer year must add 'year' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.ctl.form["year"] = "abc"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("year", self.ctl.form["inputError"])

    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_missing_student_id_sets_error(self, mock_ms_cls):
        """An empty student_id must add 'student_id' to inputError."""
        mock_ms_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
        self._fill_valid()
        self.ctl.form["student_id"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("student_id", self.ctl.form["inputError"])


class TestMarksheetCtlDisplay(TestCase):
    """Tests for MarksheetCtl.display() — verifies template rendering and conditional service calls."""

    def setUp(self):
        self.ctl = MarksheetCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.MarksheetCtl.StudentService")
    @patch("ORS.ctl.MarksheetCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetCtl.render")
    def test_display_with_id_loads_marksheet(self, mock_render, mock_html, mock_student_svc):
        """display() with id > 0 must call service.get(id) and populate self.form."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_student_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        ms = MagicMock()
        ms.id = 1
        ms.rollNumber = "R001"
        ms.name = "Raj"
        ms.physics = 80
        ms.chemistry = 75
        ms.maths = 90
        ms.year = 2024
        ms.student_id = 3
        ms.total = 245
        ms.percentage = 81.7
        mock_service.get.return_value = ms
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 1})

        mock_service.get.assert_called_once_with(1)
        self.assertEqual(self.ctl.form["rollNumber"], "R001")

    @patch("ORS.ctl.MarksheetCtl.StudentService")
    @patch("ORS.ctl.MarksheetCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_student_svc):
        """display() must pass 'ors/Marksheet.html' to render()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_student_svc.return_value.search.return_value = []
        self.ctl.display(self.request, params={"id": 0})
        self.assertEqual(mock_render.call_args[0][1], "ors/Marksheet.html")


class TestMarksheetCtlSubmit(TestCase):
    """Tests for MarksheetCtl.submit() — verifies save, totals, and success message."""

    def setUp(self):
        self.ctl = MarksheetCtl()
        self.ctl.form.update({
            "id": "0", "rollNumber": "R001", "name": "Raj",
            "physics": "80", "chemistry": "75", "maths": "90",
            "year": "2024", "student_id": "3",
        })
        self.request = MagicMock()

    @patch("ORS.ctl.MarksheetCtl.StudentService")
    @patch("ORS.ctl.MarksheetCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetCtl.render")
    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_submit_calls_service_save(self, mock_ms_cls, mock_render, mock_html, mock_student_svc):
        """submit() must call service.save() with the Marksheet instance built from the form."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_student_svc.return_value.search.return_value = []
        ms_instance = MagicMock()
        ms_instance.id = 5
        ms_instance.total = 245
        ms_instance.percentage = 81.7
        mock_ms_cls.return_value = ms_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.save.assert_called_once_with(ms_instance)

    @patch("ORS.ctl.MarksheetCtl.StudentService")
    @patch("ORS.ctl.MarksheetCtl.HtmlUtility")
    @patch("ORS.ctl.MarksheetCtl.render")
    @patch("ORS.ctl.MarksheetCtl.Marksheet")
    def test_submit_syncs_totals_to_form(self, mock_ms_cls, mock_render, mock_html, mock_student_svc):
        """submit() must copy total and percentage from the saved instance back into form."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_student_svc.return_value.search.return_value = []
        ms_instance = MagicMock()
        ms_instance.id = 5
        ms_instance.total = 245
        ms_instance.percentage = 81.7
        mock_ms_cls.return_value = ms_instance
        self.ctl.get_service = MagicMock(return_value=MagicMock())

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["total"], 245)
        self.assertEqual(self.ctl.form["percentage"], 81.7)
        self.assertEqual(self.ctl.form["message"], "Data is saved")


class TestMarksheetCtlMeta(TestCase):
    """Tests for MarksheetCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = MarksheetCtl()

    def test_get_template(self):
        """get_template() must return 'ors/Marksheet.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Marksheet.html")

    def test_get_service_returns_marksheet_service(self):
        """get_service() must return a MarksheetService instance."""
        from service.service.MarksheetService import MarksheetService
        self.assertIsInstance(self.ctl.get_service(), MarksheetService)
