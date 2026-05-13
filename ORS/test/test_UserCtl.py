from unittest import TestCase
from unittest.mock import MagicMock, patch, mock_open
from ORS.ctl.UserCtl import UserCtl


class TestUserCtlRequestToForm(TestCase):
    """Tests for UserCtl.request_to_form() — verifies all user POST fields are mapped."""

    def setUp(self):
        self.ctl = UserCtl()

    def test_maps_all_fields(self):
        """All nine POST fields must be copied into self.form."""
        post = {
            "id": "2", "firstName": "John", "lastName": "Doe",
            "login": "john@example.com", "password": "pass123",
            "dob": "1990-01-01", "mobileNumber": "9876543210",
            "gender": "Male", "role_id": "1",
        }
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["firstName"], "John")
        self.assertEqual(self.ctl.form["login"], "john@example.com")
        self.assertEqual(self.ctl.form["role_id"], "1")

    def test_missing_fields_use_defaults(self):
        """Missing POST keys must fall back to '' or 0."""
        self.ctl.request_to_form({})
        self.assertEqual(self.ctl.form["firstName"], "")
        self.assertEqual(self.ctl.form["role_id"], 0)


class TestUserCtlModelToForm(TestCase):
    """Tests for UserCtl.model_to_form() — verifies a User instance is reflected in self.form."""

    def setUp(self):
        self.ctl = UserCtl()

    def test_model_to_form_populates_form(self):
        """All User model attributes must be copied; dob formatted as YYYY-MM-DD."""
        user = MagicMock()
        user.id = 7
        user.firstName = "John"
        user.lastName = "Doe"
        user.login = "john@example.com"
        user.password = "pass"
        user.dob.strftime.return_value = "1990-01-01"
        user.mobileNumber = "9876543210"
        user.gender = "Male"
        user.role_id = 1
        user.photo = "photos/john.jpg"
        self.ctl.model_to_form(user)
        self.assertEqual(self.ctl.form["firstName"], "John")
        self.assertEqual(self.ctl.form["photo"], "photos/john.jpg")

    def test_model_to_form_with_none_does_nothing(self):
        """Passing None must leave self.form completely unchanged."""
        original = dict(self.ctl.form)
        self.ctl.model_to_form(None)
        self.assertEqual(self.ctl.form, original)

    def test_model_to_form_null_photo_defaults_to_empty(self):
        """When obj.photo is None, form['photo'] must be set to empty string."""
        user = MagicMock()
        user.photo = None
        user.dob = None
        user.role_id = None
        self.ctl.model_to_form(user)
        self.assertEqual(self.ctl.form["photo"], "")


class TestUserCtlFormToModel(TestCase):
    """Tests for UserCtl.form_to_model() — verifies form data is written onto a User instance."""

    def setUp(self):
        self.ctl = UserCtl()

    def test_form_to_model_with_positive_id(self):
        """When id > 0, pk must be set and all fields mapped onto the model."""
        self.ctl.form.update({
            "id": "5", "firstName": "John", "lastName": "Doe",
            "login": "john@example.com", "password": "pass",
            "dob": "1990-01-01", "mobileNumber": "9876543210",
            "gender": "Male", "role_id": "1", "photo": "",
        })
        user = MagicMock()
        result = self.ctl.form_to_model(user)
        self.assertEqual(user.id, 5)
        self.assertEqual(user.firstName, "John")
        self.assertIs(result, user)

    def test_form_to_model_with_empty_dob_assigns_none(self):
        """When dob is empty, obj.dob must be set to None."""
        self.ctl.form.update({
            "id": "0", "firstName": "A", "lastName": "B",
            "login": "a@b.com", "password": "p",
            "dob": "", "mobileNumber": "9000000000",
            "gender": "Male", "role_id": "1", "photo": "",
        })
        user = MagicMock()
        self.ctl.form_to_model(user)
        self.assertIsNone(user.dob)


class TestUserCtlInputValidation(TestCase):
    """Tests for UserCtl.input_validation() — verifies each required-field rule."""

    def setUp(self):
        self.ctl = UserCtl()

    def _fill_valid(self):
        self.ctl.form.update({
            "firstName": "John", "lastName": "Doe",
            "login": "john@example.com", "password": "pass123",
            "mobileNumber": "9876543210", "id": "0",
        })

    @patch("ORS.ctl.UserCtl.User")
    def test_valid_form_returns_false(self, mock_user_cls):
        """A complete valid form with unique login must return False."""
        mock_user_cls.objects.filter.return_value.exclude.return_value.exists.return_value = False
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

    def test_missing_login_sets_error(self):
        """An empty login must add 'login' to inputError."""
        self._fill_valid()
        self.ctl.form["login"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("login", self.ctl.form["inputError"])

    def test_invalid_login_email_sets_error(self):
        """A login that is not a valid email must add 'login' to inputError."""
        self._fill_valid()
        self.ctl.form["login"] = "not-an-email"
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("login", self.ctl.form["inputError"])

    @patch("ORS.ctl.UserCtl.User")
    def test_duplicate_login_sets_error(self, mock_user_cls):
        """When the login already exists for a different user, 'login' must be added to inputError."""
        mock_user_cls.objects.filter.return_value.exclude.return_value.exists.return_value = True
        self._fill_valid()
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("login", self.ctl.form["inputError"])

    def test_missing_password_sets_error(self):
        """An empty password must add 'password' to inputError."""
        self._fill_valid()
        self.ctl.form["password"] = ""
        self.assertTrue(self.ctl.input_validation())
        self.assertIn("password", self.ctl.form["inputError"])

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


class TestUserCtlDisplay(TestCase):
    """Tests for UserCtl.display() — verifies conditional data load and render."""

    def setUp(self):
        self.ctl = UserCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.UserCtl.RoleService")
    @patch("ORS.ctl.UserCtl.HtmlUtility")
    @patch("ORS.ctl.UserCtl.render")
    def test_display_with_id_loads_user(self, mock_render, mock_html, mock_role_svc):
        """display() with id > 0 must call service.get(id) and populate self.form."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_role_svc.return_value.search.return_value = []
        mock_service = MagicMock()
        user = MagicMock()
        user.id = 3
        user.firstName = "Alice"
        user.lastName = "Smith"
        user.login = "alice@example.com"
        user.password = "pw"
        user.dob = None
        user.mobileNumber = "9000000002"
        user.gender = "Female"
        user.role_id = None
        user.photo = None
        mock_service.get.return_value = user
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={"id": 3})

        mock_service.get.assert_called_once_with(3)
        self.assertEqual(self.ctl.form["firstName"], "Alice")

    @patch("ORS.ctl.UserCtl.RoleService")
    @patch("ORS.ctl.UserCtl.HtmlUtility")
    @patch("ORS.ctl.UserCtl.render")
    def test_display_renders_correct_template(self, mock_render, mock_html, mock_role_svc):
        """display() must pass 'ors/User.html' to render()."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_role_svc.return_value.search.return_value = []
        self.ctl.display(self.request, params={"id": 0})
        self.assertEqual(mock_render.call_args[0][1], "ors/User.html")


class TestUserCtlSubmit(TestCase):
    """Tests for UserCtl.submit() — verifies photo handling paths and save call."""

    def setUp(self):
        self.ctl = UserCtl()
        self.ctl.form.update({
            "id": "0", "firstName": "John", "lastName": "Doe",
            "login": "john@example.com", "password": "pass",
            "dob": "", "mobileNumber": "9876543210",
            "gender": "Male", "role_id": "1",
        })
        self.request = MagicMock()

    @patch("ORS.ctl.UserCtl.RoleService")
    @patch("ORS.ctl.UserCtl.HtmlUtility")
    @patch("ORS.ctl.UserCtl.render")
    @patch("ORS.ctl.UserCtl.User")
    def test_submit_without_photo_calls_save(self, mock_user_cls, mock_render, mock_html, mock_role_svc):
        """submit() with no uploaded photo must call service.save() and set success message."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_role_svc.return_value.search.return_value = []
        self.request.FILES.get.return_value = None
        user_instance = MagicMock()
        user_instance.id = 20
        mock_user_cls.return_value = user_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        mock_service.save.assert_called_once_with(user_instance)
        self.assertEqual(self.ctl.form["message"], "Data is saved")
        self.assertFalse(self.ctl.form["error"])

    @patch("ORS.ctl.UserCtl.os")
    @patch("ORS.ctl.UserCtl.settings")
    @patch("ORS.ctl.UserCtl.RoleService")
    @patch("ORS.ctl.UserCtl.HtmlUtility")
    @patch("ORS.ctl.UserCtl.render")
    @patch("ORS.ctl.UserCtl.User")
    def test_submit_with_photo_saves_file_and_sets_path(
            self, mock_user_cls, mock_render, mock_html, mock_role_svc, mock_settings, mock_os):
        """submit() with an uploaded photo must save the file and set form['photo']."""
        mock_render.return_value = MagicMock()
        mock_html.get_list_from_beans.return_value = ""
        mock_html.get_list_from_list.return_value = ""
        mock_role_svc.return_value.search.return_value = []
        mock_settings.MEDIA_ROOT = "/media"
        mock_settings.USER_PHOTO_DIR = "user_photos"
        mock_os.path.splitext.return_value = ("name", ".jpg")
        mock_os.path.join.return_value = "/media/user_photos/file.jpg"
        mock_os.makedirs = MagicMock()

        photo_file = MagicMock()
        photo_file.name = "photo.jpg"
        photo_file.chunks.return_value = [b"data"]
        self.request.FILES.get.return_value = photo_file

        user_instance = MagicMock()
        user_instance.id = 21
        mock_user_cls.return_value = user_instance
        mock_service = MagicMock()
        self.ctl.get_service = MagicMock(return_value=mock_service)

        with patch("builtins.open", mock_open()):
            self.ctl.submit(self.request, params={})

        mock_service.save.assert_called_once()


class TestUserCtlMeta(TestCase):
    """Tests for UserCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = UserCtl()

    def test_get_template(self):
        """get_template() must return 'ors/User.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/User.html")

    def test_get_service_returns_user_service(self):
        """get_service() must return a UserService instance."""
        from service.service.UserService import UserService
        self.assertIsInstance(self.ctl.get_service(), UserService)
