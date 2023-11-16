from django.http.response import HttpResponseForbidden


class CheckUsernameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            try:           
                request_data = request.body.decode('utf-8')
                username = request_data.get('username')

                if username:
                    if any(not c.isalnum() for c in username.replace('_', '')):
                        return HttpResponseForbidden("username cannot contain special characters []")
            
            except:
                pass

        response = self.get_response(request)
        return response
