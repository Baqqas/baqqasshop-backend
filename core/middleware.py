from django.shortcuts import redirect


class CheckOrigin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get("PATH_INFO").split('/')[1]
        origin = request.META.get('HTTP_ORIGIN')
        baqqasUrl = 'https://baqqasshop.herokuapp.com'
        adminUrl = ['baqqasadmin', 'static']

        if origin == baqqasUrl or path in adminUrl:
            response = self.get_response(request)
        else:
            response = redirect(baqqasUrl)

        return response
