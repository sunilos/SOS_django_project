from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.ChangePasswordCtl import ChangePasswordCtl


class TestChangePasswordCtlRequestToForm(TestCase):
    """Tests for ChangePasswordCtl.request_to_form() — verifies password fields are mapped."""

    def setUp(self):
        self.ctl = ChangePasswordCtl()

    def test_maps_all_password_fields(self):
        """oldPassword, newPassword, and confirmPassword must all be copied into self.form."""
        post = {"oldPassword": "old123", "newPassword": "new456", "confirmPassword": "new456"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["oldPassword"], "old123")
        self.assertEqual(self.ctl.form["newPassword"], "new456")
        self.assertEqual(self.ctl.form["confirmPassword"], "new456")

    def test_missing_fields_default_to_empty_string(self):
        """Missing password fields must default to empty string."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["oldPassword"], "")
        self.assertEqual(self.ctl.form["newPassword"], "")
        self.assertEqual(self.ctl.form["confirmPassword"], "")


class TestChangePasswordCtlInputValidation(TestCase):
    """Tests for ChangePasswordCtl.input_validation() — verifies null checks and password match."""

    def setUp(self):
        self.ctl = ChangePasswordCtl()

    def _fill_valid(self):
        self.ctl.form.update({"oldPassword": "old123", "newPassword": "new456", "confirmPassword": "new456"})

    def test_valid_passwords_return_false(self):
        """All three fields present and matching must return False (no errors)."""
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())

    def test_missing_old_password_sets_error(self):
        """An empty oldPassword must add 'oldPassword' to inputError."""
        self._fill_valid()
        self.ctl.form["oldPassword"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("oldPassword", self.ctl.form["inputError"])

    def test_missing_new_password_sets_error(self):
        """An empty newPassword must add 'newPassword' to inputError."""
        self._fill_valid()
        self.ctl.form["newPassword"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("newPassword", self.ctl.form["inputError"])

    def test_missing_confirm_password_sets_error(self):
        """An empty confirmPassword must add 'confirmPassword' to inputError."""
        self._fill_valid()
        self.ctl.form["confirmPassword"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("confirmPassword", self.ctl.form["inputError"])

    def test_mismatched_passwords_set_error(self):
        """When newPassword != confirmPassword the 'confirmPassword' error key must be set."""
        self._fill_valid()
        self.ctl.form["confirmPassword"] = "different"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("confirmPassword", self.ctl.form["inputError"])
        self.assertIn("do not match", self.ctl.form["inputError"]["confirmPassword"])

    def test_error_resets_between_calls(self):
        """A second call with valid data must clear inputError and return False."""
        self.ctl.form["oldPassword"] = ""
        self.ctl.input_validation()
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())
        self.assertEqual(self.ctl.form["inputError"], {})


class TestChangePasswordCtlDisplay(TestCase):
    """Tests for ChangePasswordCtl.display() — verifies it simply renders the form."""

    def setUp(self):
        self.ctl = ChangePasswordCtl()

    @patch("ORS.ctl.ChangePasswordCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must render 'ors/ChangePassword.html' with the current form."""
        mock_render.return_value = MagicMock()
        request = MagicMock()

        self.ctl.display(request, params={})

        mock_render.assert_called_once()
        self.assertEqual(mock_render.call_args[0][1], "ors/ChangePassword.html")


class TestChangePasswordCtlSubmit(TestCase):
    """Tests for ChangePasswordCtl.submit() — verifies session, old-password, and success paths."""

    def setUp(self):
        self.ctl = ChangePasswordCtl()
        self.ctl.form.update({"oldPassword": "old123", "newPassword": "new456", "confirmPassword": "new456"})
        self.request = MagicMock()
        self.request.session.get.return_value = 1  # loginId

    @patch("ORS.ctl.ChangePasswordCtl.render")
    def test_submit_session_expired_sets_error(self, mock_render):
        """When service.get(loginId) returns None, an error message about expired session must be set."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.get.return_value = None
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertTrue(self.ctl.form["error"])
        self.assertIn("Session expired", self.ctl.form["message"])

    @patch("ORS.ctl.ChangePasswordCtl.render")
    def test_submit_wrong_old_password_sets_error(self, mock_render):
        """When oldPassword does not match user.password, an error message must be set."""
        mock_render.return_value = MagicMock()
        user = MagicMock()
        user.password = "different"
        mock_service = MagicMock()
        mock_service.get.return_value = user
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertTrue(self.ctl.form["error"])
        self.assertIn("incorrect", self.ctl.form["message"])

    @patch("ORS.ctl.ChangePasswordCtl.render")
    def test_submit_correct_password_calls_change_password(self, mock_render):
        """When oldPassword matches, service.change_password() must be called with the new password."""
        mock_render.return_value = MagicMock()
        user = MagicMock()
        user.password = "old123"
        user.login = "user@example.com"
        mock_service = MagicMock()
        mock_service.get.return_value = user
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.change_password.assert_called_once_with("user@example.com", "new456")
        self.assertFalse(self.ctl.form["error"])
        self.assertIn("successfully", self.ctl.form["message"])


class TestChangePasswordCtlMeta(TestCase):
    """Tests for ChangePasswordCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = ChangePasswordCtl()

    def test_get_template(self):
        """get_template() must return 'ors/ChangePassword.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/ChangePassword.html")

    def test_get_service_returns_user_service(self):
        """get_service() must return a UserService instance."""
        from service.service.UserService import UserService
        self.assertIsInstance(self.ctl.get_service(), UserService)
