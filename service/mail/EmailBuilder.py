from string import Template

from SOS_django_projects.settings import BASE_DIR


class EmailBuilder:

    template_dir = BASE_DIR + "/" + "service/template/"

    @staticmethod
    def sign_up(params):
        return EmailBuilder._render("newuser.html", params)

    @staticmethod
    def change_password(params):
        return EmailBuilder._render("changepassword.html", params)

    @staticmethod
    def forgot_password(params):
        return EmailBuilder._render("forgotpassword.html", params)

    @staticmethod
    def _render(filename, params):
        with open(EmailBuilder.template_dir + filename) as f:
            return Template(f.read()).substitute(params)
