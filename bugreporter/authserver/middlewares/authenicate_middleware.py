from django.utils.deprecation import MiddlewareMixin


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.account = request.session.get('name')
