from core.utils import generate_name


class UsernameMiddleware:
    def process_request(self, request):
        username = request.session.get('username') or generate_name()
        request.username = request.session['username'] = username
