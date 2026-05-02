from django.shortcuts import redirect

PUBLIC_URLS = [
    '/',
    '/ORS/auth/Login',
    '/ORS/auth/ForgetPassword',
    '/ORS/auth/Registration',
]


class FrontController:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('user') and request.path not in PUBLIC_URLS:
            return redirect('/ORS/auth/Login')
        return self.get_response(request)
