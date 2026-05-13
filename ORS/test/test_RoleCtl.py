from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.RoleCtl import RoleCtl


class TestRoleCtlRequestToForm(TestCase):
    """Tests for RoleCtl.request_to_form() — verifies POST data is mapped into self.form."""

    def setUp(self):
        self.ctl = RoleCtl()

    def test_request_to_form_all_fields(self):
        """All three POST fields must be copied verbatim into self.form."""
        post = {"id": "3", "name": "Admin", "description": "Full access"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["id"], "3")
        self.assertEqual(self.ctl.form["name"], "Admin")
        self.assertEqual(self.ctl.form["description"], "Full access")

    def test_request_to_form_missing_fields_use_defaults(self):
        """Missing POST keys must fall back to safe defaults."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["id"], 0)
        self.assertEqual(self.ctl.form["name"], "")
        self.assertEqual(self.ctl.form["description"], "")


class TestRoleCtlModelToForm(TestCase):
    """Tests for RoleCtl.model_to_form() — verifies a Role instance is reflected in self.form."""

    def setUp(self):
        self.ctl = RoleCtl()

    def test_model_to_form_populates_form(self):
        """All Role model attributes must be copied into the corresponding form keys."""
        role = MagicMock()
        role.id = 2
        role.name = "Student"
        role.description = "Student role"
        self.ctl.model_to_form(role)
        self.assertEqual(self.ctl.form["id"], 2)
        self.assertEqual(self.ctl.form["name"], "Student")
        self.assertEqual(self.ctl.form["description"], "Student role")

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged."""
        original = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original)


class TestRoleCtlFormToModel(TestCase):
    """Tests for RoleCtl.form_to_model() — verifies form data is written onto a Role instance."""

    def setUp(self):
        self.ctl = RoleCtl()

    def test_form_to_model_with_positive_id(self):
        """When id > 0, pk must be cast to int and set together with all other fields."""
        self.ctl.form.update({"id": "5", "name": "Faculty", "description": "Teacher role"})
        role = MagicMock()
        result = self.ctl.form_to_model(role)
        self.assertEqual(role.id, 5)
        self.assertEqual(role.name, "Faculty")
        self.assertEqual(role.description, "Teacher role")
        self.assertIs(result, role)

    def test_form_to_model_with_zero_id_skips_pk_assignment(self):
        """When id == 0, obj.id must not be assigned so the DB auto-generates it."""
        self.ctl.form.update({"id": "0", "name": "Guest", "description": "Read only"})
        role = MagicMock()
        self.ctl.form_to_model(role)
        self.assertNotEqual(role.id, 0)  # id should not have been explicitly set to 0


class TestRoleCtlInputValidation(TestCase):
    """Tests for RoleCtl.input_validation() — verifies required-field rules."""

    def setUp(self):
        self.ctl = RoleCtl()

    def _fill_valid(self):
        self.ctl.form.update({"name": "Admin", "description": "Full access"})

    def test_valid_form_returns_false(self):
        """A fully populated form must return False (no errors)."""
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())

    def test_missing_name_sets_error(self):
        """An empty name must set error=True and add 'name' to inputError."""
        self._fill_valid()
        self.ctl.form["name"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("name", self.ctl.form["inputError"])

    def test_missing_description_sets_error(self):
        """An empty description must set error=True and add 'description' to inputError."""
        self._fill_valid()
        self.ctl.form["description"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("description", self.ctl.form["inputError"])

    def test_all_fields_missing_collects_both_errors(self):
        """When both fields are empty, both keys must appear in inputError."""
        # RoleCtl.input_validation() accesses form["name"] directly (not .get),
        # so the keys must exist before calling validation.
        self.ctl.form.update({"name": "", "description": ""})
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("name", self.ctl.form["inputError"])
        self.assertIn("description", self.ctl.form["inputError"])

    def test_error_state_resets_between_calls(self):
        """A second call with valid data must clear inputError and return False."""
        self.ctl.form.update({"name": "", "description": ""})
        self.ctl.input_validation()
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())
        self.assertEqual(self.ctl.form["inputError"], {})


class TestRoleCtlDisplay(TestCase):
    """Tests for RoleCtl.display() — verifies template rendering and conditional service calls."""

    def setUp(self):
        self.ctl = RoleCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.RoleCtl.render")
    def test_display_with_id_loads_role(self, mock_render):
        """display() with id > 0 must call service.get(id) and populate self.form."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        role = MagicMock()
        role.id = 1
        role.name = "Admin"
        role.description = "Desc"
        mock_service.get.return_value = role
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 1})

        mock_service.get.assert_called_once_with(1)
        self.assertEqual(self.ctl.form["name"], "Admin")

    @patch("ORS.ctl.RoleCtl.render")
    def test_display_with_zero_id_skips_service(self, mock_render):
        """display() with id == 0 must not call the service at all."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock()

        self.ctl.display(self.request, params={"id": 0})

        self.ctl.get_service.assert_not_called()

    @patch("ORS.ctl.RoleCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must pass 'ors/Role.html' to render()."""
        mock_render.return_value = MagicMock()
        self.ctl.display(self.request, params={"id": 0})
        self.assertEqual(mock_render.call_args[0][1], "ors/Role.html")


class TestRoleCtlSubmit(TestCase):
    """Tests for RoleCtl.submit() — verifies save, success state, and re-render."""

    def setUp(self):
        self.ctl = RoleCtl()
        self.ctl.form.update({"id": "0", "name": "Editor", "description": "Can edit"})
        self.request = MagicMock()

    @patch("ORS.ctl.RoleCtl.render")
    @patch("ORS.ctl.RoleCtl.Role")
    def test_submit_calls_service_save(self, mock_role_cls, mock_render):
        """submit() must pass the Role instance to service.save()."""
        mock_render.return_value = MagicMock()
        role_instance = MagicMock()
        mock_role_cls.return_value = role_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request)

        mock_service.save.assert_called_once_with(role_instance)

    @patch("ORS.ctl.RoleCtl.render")
    @patch("ORS.ctl.RoleCtl.Role")
    def test_submit_sets_success_message(self, mock_role_cls, mock_render):
        """submit() must set form['message'] = 'Data is saved' and form['error'] = False."""
        mock_render.return_value = MagicMock()
        mock_role_cls.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=MagicMock())

        self.ctl.submit(self.request)

        self.assertEqual(self.ctl.form["message"], "Data is saved")
        self.assertFalse(self.ctl.form["error"])

    @patch("ORS.ctl.RoleCtl.render")
    @patch("ORS.ctl.RoleCtl.Role")
    def test_submit_syncs_role_id_to_form(self, mock_role_cls, mock_render):
        """submit() must copy the DB-assigned role.id back into form['id'] after save."""
        mock_render.return_value = MagicMock()
        role_instance = MagicMock()
        role_instance.id = 99
        mock_role_cls.return_value = role_instance
        self.ctl.get_service = MagicMock(return_value=MagicMock())

        self.ctl.submit(self.request)

        self.assertEqual(self.ctl.form["id"], 99)


class TestRoleCtlMeta(TestCase):
    """Tests for RoleCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = RoleCtl()

    def test_get_template_returns_correct_path(self):
        """get_template() must return 'ors/Role.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Role.html")

    def test_get_service_returns_role_service(self):
        """get_service() must return a RoleService instance."""
        from service.service.RoleService import RoleService
        self.assertIsInstance(self.ctl.get_service(), RoleService)
