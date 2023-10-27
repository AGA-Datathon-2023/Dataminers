from django.http import HttpResponse
from django.conf import settings
import os, io

_STATIC_ROOT = settings.STATIC_ROOT
_STATIC_URL = settings.STATIC_URL

assert _STATIC_ROOT is not None and _STATIC_URL is not None

def save_file(stream: io.IOBase, path):
    with open(os.path.join(_STATIC_ROOT, path), 'wb+') as destination:
        destination.write(stream.read())


def serve_file(path) ->  HttpResponse:
    return HttpResponse(open(os.path.join(_STATIC_ROOT, path), 'rb').read(), content_type='application/octet-stream')