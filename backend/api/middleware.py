import re

class ApiVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        version_match = re.search(r'/api/v(\d+)', request.path)
        version = version_match.group(1) if version_match else '1'

        request.api_version = version #for accessing in views

        response = self.get_response(request)
        response['X-API-Version'] = version
        return response