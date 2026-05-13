from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.LoginCtl import LoginCtl


class TestLoginCtlRequestToForm(TestCase):
    """Tests for LoginCtl.request_to_form() — verifies POST credentials are mapped."""

    def setUp(self):
        self.ctl = LoginCtl()

    def test_maps_all_credential_fields(self):
        """loginId, password, and rememberMe must all be read from the request dict."""
        post = {"loginId": "user@example.com", "password": "secret", "rememberMe": "on"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["loginId"], "user@example.com")
        self.assertEqual(self.ctl.form["password"], "secret")
        self.assertEqual(self.ctl.form["rememberMe"], "on")

    def test_remember_me_defaults_to_false(self):
        """When rememberMe is absent from the POST, it must default to False."""
        self.ctl.request_to_form({"loginId": "u", "password": "p"})
        self.assertFalse(self.ctl.form["rememberMe"])


class TestLoginCtlInputValidation(TestCase):
    """Tests for LoginCtl.input_validation() — verifies credential null checks."""

    def setUp(self):
        self.ctl = LoginCtl()

    def _fill_valid(self):
        self.ctl.form.update({"loginId": "user@example.com", "password": "secret"})

    def test_valid_credentials_return_false(self):
        """Both fields present must return False (no errors)."""
        self._fill_valid()
        self.assertFalse(self.ctl.input_validation())

    def test_missing_login_id_sets_error(self):
        """An empty loginId must add 'loginId' to inputError."""
        self._fill_valid()
        self.ctl.form["loginId"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("loginId", self.ctl.form["inputError"])

    def test_missing_password_sets_error(self):
        """An empty password must add 'password' to inputError."""
        self._fill_valid()
        self.ctl.form["password"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("password", self.ctl.form["inputError"])

    def test_both_missing_collects_both_errors(self):
        """When both fields are empty, both keys must appear in inputError."""
        self.ctl.form.update({"loginId": "", "password": ""})
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("loginId", self.ctl.form["inputError"])
        self.assertIn("password", self.ctl.form["inputError"])


class TestLoginCtlDisplay(TestCase):
    """Tests for LoginCtl.display() — verifies redirect when already logged in."""

    def setUp(self):
        self.ctl = LoginCtl()

    @patch("ORS.ctl.LoginCtl.redirect")
    def test_display_with_active_session_redirects(self, mock_redirect):
        """When 'loginId' exists in the session, display() must redirect to Welcome."""
        mock_redirect.return_value = MagicMock()
        request = MagicMock()
        request.session.get.return_value = 42  # loginId is set

        self.ctl.display(request, params={})

        mock_redirect.assert_called_once_with("/ORS/Welcome")

    @patch("ORS.ctl.LoginCtl.render")
    def test_display_without_session_renders_login_page(self, mock_render):
        """When 'loginId' is absent from the session, display() must render the login form."""
        mock_render.return_value = MagicMock()
        request = MagicMock()
        request.session.get.return_value = None

        self.ctl.display(request, params={})

        mock_render.assert_called_once()
        self.assertEqual(mock_render.call_args[0][1], "ors/Login.html")


class TestLoginCtlSubmit(TestCase):
    """Tests for LoginCtl.submit() — verifies authentication flow and session setup."""

    def setUp(self):
        self.ctl = LoginCtl()
        self.ctl.form.update({"loginId": "user@example.com", "password": "secret", "rememberMe": False})
        self.request = MagicMock()
        self.request.session = MagicMock()

    @patch("ORS.ctl.LoginCtl.redirect")
    def test_submit_valid_credentials_sets_session_and_redirects(self, mock_redirect):
        """Valid credentials must store user details in the session and redirect to Welcome."""
        mock_redirect.return_value = MagicMock()
        user = MagicMock()
        user.login = "user@example.com"
        user.id = 1
        user.firstName = "John"
        user.lastName = "Doe"
        mock_service = MagicMock()
        mock_service.authenticate.return_value = user
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        # session["key"] = val translates to __setitem__(key, val) on the MagicMock
        self.request.session.__setitem__.assert_any_call("user", "user@example.com")
        self.request.session.__setitem__.assert_any_call("loginId", 1)
        mock_redirect.assert_called_once_with("/ORS/Welcome")

    @patch("ORS.ctl.LoginCtl.render")
    def test_submit_invalid_credentials_sets_error_message(self, mock_render):
        """When authenticate() returns None, form['message'] must be set and login page re-rendered."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.authenticate.return_value = None
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertIn("Invalid", self.ctl.form["message"])
        mock_render.assert_called_once()

    @patch("ORS.ctl.LoginCtl.render")
    def test_submit_with_validation_failure_renders_without_auth(self, mock_render):
        """When input_validation fails, submit() must re-render the form without calling authenticate()."""
        mock_render.return_value = MagicMock()
        self.ctl.form.update({"loginId": "", "password": ""})
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.authenticate.assert_not_called()
        mock_render.assert_called_once()


class TestLoginCtlMeta(TestCase):
    """Tests for LoginCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = LoginCtl()

    def test_get_template(self):
        """get_template() must return 'ors/Login.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Login.html")

    def test_get_service_returns_user_service(self):
        """get_service() must return a UserService instance."""
        from service.service.UserService import UserService
        self.assertIsInstance(self.ctl.get_service(), UserService)
