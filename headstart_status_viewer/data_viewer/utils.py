import json
import numpy as np
from datetime import datetime
from django.http import HttpRequest, HttpResponse
from .models import Transaction

class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.astimezone().isoformat()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        else:
            return super().default(obj)
        


def log_event(request: HttpRequest, status_code: int):
    try:
        ip = request.META.get('REMOTE_ADDR')
        device = request.META.get('HTTP_USER_AGENT')
        params = request.GET.dict() or request.POST.dict()
        path = request.path
        met = request.method
        new_record = Transaction(ip = ip, device= device, method=met, path=path, params=params, status_code=status_code)
        new_record.save()
    except Exception as e:
        raise e
    

def logger(func):
    def wrapper(request: HttpRequest, **kwargs):
        try:
            response = func(request, **kwargs)
            status_code = response.status_code
            log_event(request, status_code)
            return response
        except Exception as e:
            raise e
    return wrapper