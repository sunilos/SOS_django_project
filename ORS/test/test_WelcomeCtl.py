from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.WelcomeCtl import WelcomeCtl


class TestWelcomeCtlDisplay(TestCase):
    """Tests for WelcomeCtl.display() — verifies session-based welcome message."""

    def setUp(self):
        self.ctl = WelcomeCtl()

    @patch("ORS.ctl.WelcomeCtl.render")
    def test_display_with_logged_in_user_sets_welcome_message(self, mock_render):
        """When 'user' is in the session, form['message'] must greet that user by name."""
        mock_render.return_value = MagicMock()
        request = MagicMock()
        request.session.get.return_value = "alice@example.com"

        self.ctl.display(request, params={})

        self.assertIn("alice@example.com", self.ctl.form["message"])
        mock_render.assert_called_once()

    @patch("ORS.ctl.WelcomeCtl.render")
    def test_display_without_session_user_leaves_default_message(self, mock_render):
        """When no 'user' key is in the session, form['message'] must remain the default empty string."""
        mock_render.return_value = MagicMock()
        request = MagicMock()
        request.session.get.return_value = None

        self.ctl.display(request, params={})

        self.assertEqual(self.ctl.form["message"], "")

    @patch("ORS.ctl.WelcomeCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must pass 'ors/Welcome.html' to render()."""
        mock_render.return_value = MagicMock()
        request = MagicMock()
        request.session.get.return_value = None

        self.ctl.display(request, params={})

        args, _ = mock_render.call_args
        self.assertEqual(args[1], "ors/Welcome.html")


class TestWelcomeCtlSubmit(TestCase):
    """Tests for WelcomeCtl.submit() — verifies it renders the welcome template."""

    def setUp(self):
        self.ctl = WelcomeCtl()

    @patch("ORS.ctl.WelcomeCtl.render")
    def test_submit_renders_correct_template(self, mock_render):
        """submit() must render 'ors/Welcome.html' with the current form."""
        mock_render.return_value = MagicMock()
        request = MagicMock()

        self.ctl.submit(request, params={})

        args, _ = mock_render.call_args
        self.assertEqual(args[1], "ors/Welcome.html")


class TestWelcomeCtlMeta(TestCase):
    """Tests for WelcomeCtl factory methods."""

    def setUp(self):
        self.ctl = WelcomeCtl()

    def test_get_template_returns_correct_path(self):
        """get_template() must return 'ors/Welcome.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Welcome.html")

    def test_get_service_returns_string_stub(self):
        """get_service() currently returns a string stub (not yet wired to a real service)."""
        self.assertEqual(self.ctl.get_service(), "RoleService()")
