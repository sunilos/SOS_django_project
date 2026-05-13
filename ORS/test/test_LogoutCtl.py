from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.LogoutCtl import LogoutCtl


class TestLogoutCtlDisplay(TestCase):
    """Tests for LogoutCtl.display() — verifies session is flushed and user is redirected."""

    def setUp(self):
        self.ctl = LogoutCtl()

    @patch("ORS.ctl.LogoutCtl.redirect")
    def test_display_flushes_session(self, mock_redirect):
        """display() must call request.session.flush() to clear the session."""
        mock_redirect.return_value = MagicMock()
        request = MagicMock()

        self.ctl.display(request)

        request.session.flush.assert_called_once()

    @patch("ORS.ctl.LogoutCtl.redirect")
    def test_display_redirects_to_login(self, mock_redirect):
        """display() must redirect to '/ORS/Login' after flushing the session."""
        mock_redirect.return_value = MagicMock()
        request = MagicMock()

        self.ctl.display(request)

        mock_redirect.assert_called_once_with("/ORS/Login")


class TestLogoutCtlSubmit(TestCase):
    """Tests for LogoutCtl.submit() — verifies same flush-and-redirect behaviour as display."""

    def setUp(self):
        self.ctl = LogoutCtl()

    @patch("ORS.ctl.LogoutCtl.redirect")
    def test_submit_flushes_session(self, mock_redirect):
        """submit() must call request.session.flush() to clear the session."""
        mock_redirect.return_value = MagicMock()
        request = MagicMock()

        self.ctl.submit(request)

        request.session.flush.assert_called_once()

    @patch("ORS.ctl.LogoutCtl.redirect")
    def test_submit_redirects_to_login(self, mock_redirect):
        """submit() must redirect to '/ORS/Login' after flushing the session."""
        mock_redirect.return_value = MagicMock()
        request = MagicMock()

        self.ctl.submit(request)

        mock_redirect.assert_called_once_with("/ORS/Login")


class TestLogoutCtlMeta(TestCase):
    """Tests for LogoutCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = LogoutCtl()

    def test_get_template(self):
        """get_template() must return 'ors/Login.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/Login.html")

    def test_get_service_returns_none(self):
        """get_service() is a no-op stub and must return None."""
        self.assertIsNone(self.ctl.get_service())
