from django.http import HttpRequest, HttpResponse


def SimpleAntiScrapperMdw(get_response):

    def is_scrapper(req: HttpRequest):
        return not bool(req.headers.get('User-Agent', None))

    def middleware(request: HttpRequest):

        if is_scrapper(request):
            return HttpResponse(status=403)
        else:
            response = get_response(request)
            return response

    return middleware