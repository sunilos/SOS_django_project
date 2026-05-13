from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.ForgetPasswordCtl import ForgetPasswordCtl


class TestForgetPasswordCtlRequestToForm(TestCase):
    """Tests for ForgetPasswordCtl.request_to_form() — verifies loginId is mapped."""

    def setUp(self):
        self.ctl = ForgetPasswordCtl()

    def test_maps_login_id(self):
        """loginId must be copied from the request dict into self.form."""
        self.ctl.request_to_form({"loginId": "user@example.com"})
        self.assertEqual(self.ctl.form["loginId"], "user@example.com")

    def test_missing_login_id_defaults_to_empty(self):
        """Missing loginId must default to an empty string."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["loginId"], "")


class TestForgetPasswordCtlInputValidation(TestCase):
    """Tests for ForgetPasswordCtl.input_validation() — verifies null check on loginId."""

    def setUp(self):
        self.ctl = ForgetPasswordCtl()

    def test_valid_login_id_returns_false(self):
        """A non-empty loginId must return False (no error)."""
        self.ctl.form["loginId"] = "user@example.com"
        self.assertFalse(self.ctl.input_validation())

    def test_missing_login_id_sets_error(self):
        """An empty loginId must add 'loginId' to inputError and return True."""
        self.ctl.form["loginId"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("loginId", self.ctl.form["inputError"])

    def test_error_resets_between_calls(self):
        """A second call with a valid loginId must clear inputError and return False."""
        self.ctl.form["loginId"] = ""
        self.ctl.input_validation()
        self.ctl.form["loginId"] = "user@example.com"
        self.assertFalse(self.ctl.input_validation())
        self.assertEqual(self.ctl.form["inputError"], {})


class TestForgetPasswordCtlDisplay(TestCase):
    """Tests for ForgetPasswordCtl.display() — verifies it renders the forget-password page."""

    def setUp(self):
        self.ctl = ForgetPasswordCtl()

    @patch("ORS.ctl.ForgetPasswordCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must render 'ors/ForgetPassword.html' with the current form."""
        mock_render.return_value = MagicMock()
        request = MagicMock()

        self.ctl.display(request, params={})

        mock_render.assert_called_once()
        self.assertEqual(mock_render.call_args[0][1], "ors/ForgetPassword.html")


class TestForgetPasswordCtlSubmit(TestCase):
    """Tests for ForgetPasswordCtl.submit() — verifies found / not-found messaging."""

    def setUp(self):
        self.ctl = ForgetPasswordCtl()
        self.ctl.form["loginId"] = "user@example.com"
        self.request = MagicMock()

    @patch("ORS.ctl.ForgetPasswordCtl.render")
    def test_submit_found_user_sets_sent_message(self, mock_render):
        """When forgot_password() returns a user, form['message'] must confirm an email was sent."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.forgot_password.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertIn("sent", self.ctl.form["message"])

    @patch("ORS.ctl.ForgetPasswordCtl.render")
    def test_submit_not_found_user_sets_not_exist_message(self, mock_render):
        """When forgot_password() returns None, form['message'] must state the login ID does not exist."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.forgot_password.return_value = None
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertIn("does not exist", self.ctl.form["message"])

    @patch("ORS.ctl.ForgetPasswordCtl.render")
    def test_submit_with_empty_login_id_skips_service(self, mock_render):
        """When input validation fails (empty loginId), the service must not be called."""
        mock_render.return_value = MagicMock()
        self.ctl.form["loginId"] = ""
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.forgot_password.assert_not_called()


class TestForgetPasswordCtlMeta(TestCase):
    """Tests for ForgetPasswordCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = ForgetPasswordCtl()

    def test_get_template(self):
        """get_template() must return 'ors/ForgetPassword.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/ForgetPassword.html")

    def test_get_service_returns_user_service(self):
        """get_service() must return a UserService instance."""
        from service.service.UserService import UserService
        self.assertIsInstance(self.ctl.get_service(), UserService)
