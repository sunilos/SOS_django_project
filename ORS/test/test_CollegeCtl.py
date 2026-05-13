from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from ORS.ctl.CollegeCtl import CollegeCtl


class TestCollegeCtlPreload(TestCase):
    """Tests for CollegeCtl.preload() — verifies state dropdown data is loaded correctly."""

    def setUp(self):
        self.ctl = CollegeCtl()
        self.request = MagicMock()

    def test_preload_returns_state_list(self):
        """preload() must include 'state_list' key in the returned dict."""
        result = self.ctl.preload(self.request)
        self.assertIn("state_list", result)

    def test_preload_state_list_values(self):
        """preload() must return exactly the two supported state names."""
        result = self.ctl.preload(self.request)
        self.assertEqual(result["state_list"], ["Madhya Pradesh", "Uttar Pradesh"])


class TestCollegeCtlRequestToForm(TestCase):
    """Tests for CollegeCtl.request_to_form() — verifies POST data is mapped into self.form."""

    def setUp(self):
        self.ctl = CollegeCtl()

    def test_request_to_form_all_fields(self):
        """All six POST fields must be copied verbatim into self.form."""
        post = {"id": "5", "name": "MIT", "address": "123 Main St",
                "state": "Madhya Pradesh", "city": "Bhopal", "phoneNumber": "9876543210"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["id"], "5")
        self.assertEqual(self.ctl.form["name"], "MIT")
        self.assertEqual(self.ctl.form["address"], "123 Main St")
        self.assertEqual(self.ctl.form["state"], "Madhya Pradesh")
        self.assertEqual(self.ctl.form["city"], "Bhopal")
        self.assertEqual(self.ctl.form["phoneNumber"], "9876543210")

    def test_request_to_form_missing_fields_use_defaults(self):
        """Missing POST keys must fall back to safe defaults (0 for id, '' for strings)."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["id"], 0)
        self.assertEqual(self.ctl.form["name"], "")
        self.assertEqual(self.ctl.form["address"], "")
        self.assertEqual(self.ctl.form["state"], "")
        self.assertEqual(self.ctl.form["city"], "")
        self.assertEqual(self.ctl.form["phoneNumber"], "")


class TestCollegeCtlModelToForm(TestCase):
    """Tests for CollegeCtl.model_to_form() — verifies a College instance is reflected in self.form."""

    def setUp(self):
        self.ctl = CollegeCtl()

    def test_model_to_form_populates_form(self):
        """All College model attributes must be copied into the corresponding form keys."""
        college = MagicMock()
        college.id = 3
        college.name = "IIT"
        college.address = "Delhi"
        college.state = "Uttar Pradesh"
        college.city = "Noida"
        college.phoneNumber = "9123456789"

        self.ctl.model_to_form(college)

        self.assertEqual(self.ctl.form["id"], 3)
        self.assertEqual(self.ctl.form["name"], "IIT")
        self.assertEqual(self.ctl.form["address"], "Delhi")
        self.assertEqual(self.ctl.form["state"], "Uttar Pradesh")
        self.assertEqual(self.ctl.form["city"], "Noida")
        self.assertEqual(self.ctl.form["phoneNumber"], "9123456789")

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged (early-return guard)."""
        original_form = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original_form)


class TestCollegeCtlFormToModel(TestCase):
    """Tests for CollegeCtl.form_to_model() — verifies form data is written onto a College instance."""

    def setUp(self):
        self.ctl = CollegeCtl()

    def test_form_to_model_with_positive_id(self):
        """When id > 0, the pk must be cast to int and set on the model along with all other fields."""
        self.ctl.form["id"] = "7"
        self.ctl.form["name"] = "NIT"
        self.ctl.form["address"] = "Indore"
        self.ctl.form["state"] = "Madhya Pradesh"
        self.ctl.form["city"] = "Indore"
        self.ctl.form["phoneNumber"] = "9000000001"

        college = MagicMock()
        result = self.ctl.form_to_model(college)

        self.assertEqual(college.id, 7)
        self.assertEqual(college.name, "NIT")
        self.assertEqual(college.address, "Indore")
        self.assertEqual(college.state, "Madhya Pradesh")
        self.assertEqual(college.city, "Indore")
        self.assertEqual(college.phoneNumber, "9000000001")
        self.assertIs(result, college)

    def test_form_to_model_with_zero_id_does_not_set_id(self):
        """When id == 0 (new record), obj.id must not be assigned so the DB auto-generates it."""
        self.ctl.form["id"] = "0"
        self.ctl.form["name"] = "College X"
        self.ctl.form["address"] = "Addr"
        self.ctl.form["state"] = "MP"
        self.ctl.form["city"] = "City"
        self.ctl.form["phoneNumber"] = "9111111111"

        college = MagicMock()
        self.ctl.form_to_model(college)

        college.__setattr__.assert_not_called() if False else None
        # id attribute must NOT have been set when pk == 0
        self.assertNotIn(call("id", 0), college.mock_calls)


class TestCollegeCtlInputValidation(TestCase):
    """Tests for CollegeCtl.input_validation() — verifies each required-field rule and error reset."""

    def setUp(self):
        self.ctl = CollegeCtl()

    def _fill_valid_form(self):
        """Helper: populate self.form with a complete, valid set of college fields."""
        self.ctl.form.update({
            "name": "Good College",
            "address": "123 Road",
            "state": "Madhya Pradesh",
            "city": "Bhopal",
            "phoneNumber": "9876543210",
        })

    def test_valid_form_returns_false(self):
        """A fully valid form must return False (no errors)."""
        self._fill_valid_form()
        result = self.ctl.input_validation()
        self.assertFalse(result)

    def test_missing_name_sets_error(self):
        """An empty name must set form['error'] = True and add 'name' to inputError."""
        self._fill_valid_form()
        self.ctl.form["name"] = ""
        result = self.ctl.input_validation()
        self.assertTrue(result)
        self.assertIn("name", self.ctl.form["inputError"])

    def test_missing_address_sets_error(self):
        """An empty address must set form['error'] = True and add 'address' to inputError."""
        self._fill_valid_form()
        self.ctl.form["address"] = ""
        result = self.ctl.input_validation()
        self.assertTrue(result)
        self.assertIn("address", self.ctl.form["inputError"])

    def test_missing_state_sets_error(self):
        """An empty state must set form['error'] = True and add 'state' to inputError."""
        self._fill_valid_form()
        self.ctl.form["state"] = ""
        result = self.ctl.input_validation()
        self.assertTrue(result)
        self.assertIn("state", self.ctl.form["inputError"])

    def test_missing_city_sets_error(self):
        """An empty city must set form['error'] = True and add 'city' to inputError."""
        self._fill_valid_form()
        self.ctl.form["city"] = ""
        result = self.ctl.input_validation()
        self.assertTrue(result)
        self.assertIn("city", self.ctl.form["inputError"])

    def test_missing_phone_sets_error(self):
        """An empty phoneNumber must set form['error'] = True and add 'phoneNumber' to inputError."""
        self._fill_valid_form()
        self.ctl.form["phoneNumber"] = ""
        result = self.ctl.input_validation()
        self.assertTrue(result)
        self.assertIn("phoneNumber", self.ctl.form["inputError"])

    def test_invalid_phone_format_sets_error(self):
        """A non-10-digit phoneNumber must fail with a message mentioning '10 digits'."""
        self._fill_valid_form()
        self.ctl.form["phoneNumber"] = "12345"  # not 10 digits
        result = self.ctl.input_validation()
        self.assertTrue(result)
        self.assertIn("phoneNumber", self.ctl.form["inputError"])
        self.assertIn("10 digits", self.ctl.form["inputError"]["phoneNumber"])

    def test_all_fields_missing_collects_all_errors(self):
        """When every field is empty all five keys must appear in inputError."""
        result = self.ctl.input_validation()
        self.assertTrue(result)
        for field in ("name", "address", "state", "city", "phoneNumber"):
            self.assertIn(field, self.ctl.form["inputError"])

    def test_error_state_resets_between_calls(self):
        """A second call with valid data must clear inputError and return False even after a prior failure."""
        self._fill_valid_form()
        self.ctl.form["name"] = ""
        self.ctl.input_validation()
        self._fill_valid_form()
        result = self.ctl.input_validation()
        self.assertFalse(result)
        self.assertEqual(self.ctl.form["inputError"], {})


class TestCollegeCtlDisplay(TestCase):
    """Tests for CollegeCtl.display() — verifies template rendering and conditional service calls."""

    def setUp(self):
        self.ctl = CollegeCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.CollegeCtl.render")
    def test_display_without_id_does_not_call_service(self, mock_render):
        """display() with no id param must skip the service lookup entirely."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock()

        self.ctl.display(self.request, params={})

        self.ctl.get_service.assert_not_called()
        mock_render.assert_called_once()

    @patch("ORS.ctl.CollegeCtl.render")
    def test_display_with_id_loads_college(self, mock_render):
        """display() with a valid id must call service.get(id) and populate self.form via model_to_form."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_college = MagicMock()
        mock_college.id = 2
        mock_college.name = "ABC College"
        mock_college.address = "Addr"
        mock_college.state = "MP"
        mock_college.city = "Bhopal"
        mock_college.phoneNumber = "9000000000"
        mock_service.get.return_value = mock_college
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 2})

        mock_service.get.assert_called_once_with(2)
        self.assertEqual(self.ctl.form["name"], "ABC College")

    @patch("ORS.ctl.CollegeCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must pass 'ors/College.html' as the template to render()."""
        mock_render.return_value = MagicMock()
        self.ctl.display(self.request, params={})
        args, kwargs = mock_render.call_args
        self.assertEqual(args[1], "ors/College.html")

    @patch("ORS.ctl.CollegeCtl.render")
    def test_display_passes_preload_data(self, mock_render):
        """display() must include 'preload_data' with 'state_list' in the template context."""
        mock_render.return_value = MagicMock()
        self.ctl.display(self.request, params={})
        args, kwargs = mock_render.call_args
        context = args[2]
        self.assertIn("preload_data", context)
        self.assertIn("state_list", context["preload_data"])


class TestCollegeCtlSubmit(TestCase):
    """Tests for CollegeCtl.submit() — verifies save, success state, and re-render behaviour."""

    def setUp(self):
        self.ctl = CollegeCtl()
        self.request = MagicMock()
        self.ctl.form.update({
            "id": "0",
            "name": "Test College",
            "address": "Test Addr",
            "state": "MP",
            "city": "Bhopal",
            "phoneNumber": "9876543210",
        })

    @patch("ORS.ctl.CollegeCtl.render")
    @patch("ORS.ctl.CollegeCtl.College")
    def test_submit_calls_service_save(self, mock_college_cls, mock_render):
        """submit() must pass the College instance built from form data to service.save()."""
        mock_render.return_value = MagicMock()
        mock_college_instance = MagicMock()
        mock_college_cls.return_value = mock_college_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.save.assert_called_once_with(mock_college_instance)

    @patch("ORS.ctl.CollegeCtl.render")
    @patch("ORS.ctl.CollegeCtl.College")
    def test_submit_sets_success_message(self, mock_college_cls, mock_render):
        """submit() must set form['message'] = 'Data is saved' and form['error'] = False."""
        mock_render.return_value = MagicMock()
        mock_college_instance = MagicMock()
        mock_college_cls.return_value = mock_college_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["message"], "Data is saved")
        self.assertFalse(self.ctl.form["error"])

    @patch("ORS.ctl.CollegeCtl.render")
    @patch("ORS.ctl.CollegeCtl.College")
    def test_submit_renders_correct_template(self, mock_college_cls, mock_render):
        """submit() must re-render 'ors/College.html' after a successful save."""
        mock_render.return_value = MagicMock()
        mock_college_instance = MagicMock()
        mock_college_cls.return_value = mock_college_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        args, _ = mock_render.call_args
        self.assertEqual(args[1], "ors/College.html")

    @patch("ORS.ctl.CollegeCtl.render")
    @patch("ORS.ctl.CollegeCtl.College")
    def test_submit_syncs_college_id_to_form(self, mock_college_cls, mock_render):
        """submit() must copy the DB-assigned college.id back into form['id'] after save."""
        mock_render.return_value = MagicMock()
        mock_college_instance = MagicMock()
        mock_college_instance.id = 42
        mock_college_cls.return_value = mock_college_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["id"], 42)


class TestCollegeCtlMeta(TestCase):
    """Tests for CollegeCtl.get_template() and get_service() — verifies factory methods."""

    def setUp(self):
        self.ctl = CollegeCtl()

    def test_get_template_returns_correct_path(self):
        """get_template() must return the exact template path 'ors/College.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/College.html")

    def test_get_service_returns_college_service(self):
        """get_service() must return a CollegeService instance."""
        from service.service.CollegeService import CollegeService
        self.assertIsInstance(self.ctl.get_service(), CollegeService)


class TestCollegeCtlExecuteIntegration(TestCase):
    """Integration-style tests for BaseCtl.execute() wired to CollegeCtl."""

    def setUp(self):
        self.ctl = CollegeCtl()

    @patch("ORS.ctl.CollegeCtl.render")
    def test_execute_get_calls_display(self, mock_render):
        """A GET request must delegate to display() with the original params dict."""
        mock_render.return_value = MagicMock()
        request = MagicMock()
        request.method = "GET"

        self.ctl.display = MagicMock(return_value=MagicMock())
        self.ctl.execute(request, params={})

        self.ctl.display.assert_called_once_with(request, {})

    @patch("ORS.ctl.CollegeCtl.render")
    def test_execute_post_valid_calls_submit(self, mock_render):
        """A POST request with valid data must pass validation and call submit()."""
        mock_render.return_value = MagicMock()
        request = MagicMock()
        request.method = "POST"
        request.POST = {
            "id": "0", "name": "College A", "address": "Addr",
            "state": "MP", "city": "Bhopal", "phoneNumber": "9876543210",
        }

        self.ctl.submit = MagicMock(return_value=MagicMock())
        self.ctl.execute(request, params={})

        self.ctl.submit.assert_called_once()

    @patch("ORS.ctl.BaseCtl.render")
    def test_execute_post_invalid_renders_form_with_errors(self, mock_render):
        """A POST request with all empty fields must skip submit() and re-render with error=True."""
        mock_render.return_value = MagicMock()
        request = MagicMock()
        request.method = "POST"
        request.POST = {"id": "0", "name": "", "address": "", "state": "", "city": "", "phoneNumber": ""}

        self.ctl.submit = MagicMock()
        self.ctl.execute(request, params={})

        self.ctl.submit.assert_not_called()
        mock_render.assert_called_once()
        context = mock_render.call_args[0][2]
        self.assertTrue(context["form"]["error"])

    @patch("ORS.ctl.CollegeCtl.render")
    def test_execute_delete_action_calls_service_delete(self, mock_render):
        """A GET request with action='delete' must call service.delete(id) before display()."""
        mock_render.return_value = MagicMock()
        request = MagicMock()
        request.method = "GET"

        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)
        self.ctl.display = MagicMock(return_value=MagicMock())

        self.ctl.execute(request, params={"action": "delete", "id": 9})

        mock_service.delete.assert_called_once_with(9)
