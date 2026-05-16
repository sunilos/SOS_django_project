from unittest import TestCase
from unittest.mock import MagicMock, patch
from ORS.ctl.CollegeListCtl import CollegeListCtl


class TestCollegeListCtlRequestToForm(TestCase):
    """Tests for CollegeListCtl.request_to_form() — verifies filter fields are mapped."""

    def setUp(self):
        self.ctl = CollegeListCtl()

    def test_maps_all_filter_fields(self):
        """All five college filter fields must be copied into self.form."""
        post = {"name": "MIT", "address": "Addr", "state": "MP", "city": "Bhopal", "phoneNumber": "9000000000"}
        self.ctl.request_to_form(post)
        self.assertEqual(self.ctl.form["name"], "MIT")
        self.assertEqual(self.ctl.form["address"], "Addr")
        self.assertEqual(self.ctl.form["state"], "MP")
        self.assertEqual(self.ctl.form["city"], "Bhopal")
        self.assertEqual(self.ctl.form["phoneNumber"], "9000000000")

    def test_missing_fields_default_to_none(self):
        """Missing filter keys must default to None."""
        self.ctl.request_to_form({})
        for field in ("name", "address", "state", "city", "phoneNumber"):
            self.assertIsNone(self.ctl.form[field])


class TestCollegeListCtlDisplay(TestCase):
    """Tests for CollegeListCtl.display() — verifies search and render on GET."""

    def setUp(self):
        self.ctl = CollegeListCtl()
        self.request = MagicMock()

    @patch("ORS.ctl.CollegeListCtl.render")
    def test_display_calls_search_and_renders(self, mock_render):
        """display() must call service.search() and pass results as 'pageList' to the template."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.search.return_value = ["college1"]
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.display(self.request, params={})

        mock_service.search.assert_called_once_with(self.ctl.form, page_number=1)
        context = mock_render.call_args[0][2]
        self.assertEqual(context["pageList"], ["college1"])

    @patch("ORS.ctl.CollegeListCtl.render")
    def test_display_renders_correct_template(self, mock_render):
        """display() must render 'ors/CollegeList.html'."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.display(self.request, params={})
        self.assertEqual(mock_render.call_args[0][1], "ors/CollegeList.html")


class TestCollegeListCtlSubmit(TestCase):
    """Tests for CollegeListCtl.submit() — verifies search-on-POST with form in context."""

    def setUp(self):
        self.ctl = CollegeListCtl()
        self.request = MagicMock()
        self.request.POST = {"name": "NIT", "address": "Indore", "state": "MP",
                             "city": "Indore", "phoneNumber": "9111111111"}

    @patch("ORS.ctl.CollegeListCtl.render")
    def test_submit_populates_form_and_searches(self, mock_render):
        """submit() must read POST data then call service.search()."""
        mock_render.return_value = MagicMock()
        mock_service = MagicMock()
        mock_service.search.return_value = []
        self.ctl.get_service = MagicMock(return_value=mock_service)

        self.ctl.submit(self.request, params={})

        self.assertEqual(self.ctl.form["name"], "NIT")
        mock_service.search.assert_called_once()

    @patch("ORS.ctl.CollegeListCtl.render")
    def test_submit_includes_form_in_context(self, mock_render):
        """submit() must pass both 'pageList' and 'form' to the template."""
        mock_render.return_value = MagicMock()
        self.ctl.get_service = MagicMock(return_value=MagicMock())
        self.ctl.submit(self.request, params={})
        context = mock_render.call_args[0][2]
        self.assertIn("pageList", context)
        self.assertIn("form", context)


class TestCollegeListCtlMeta(TestCase):
    """Tests for CollegeListCtl.get_template() and get_service()."""

    def setUp(self):
        self.ctl = CollegeListCtl()

    def test_get_template(self):
        """get_template() must return 'ors/CollegeList.html'."""
        self.assertEqual(self.ctl.get_template(), "ors/CollegeList.html")

    def test_get_service_returns_college_service(self):
        """get_service() must return a CollegeService instance."""
        from service.service.CollegeService import CollegeService
        self.assertIsInstance(self.ctl.get_service(), CollegeService)
