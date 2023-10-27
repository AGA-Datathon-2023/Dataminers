from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .dataPipeline import data_factory
from .models import Transaction
import json
from datetime import datetime
import numpy as np

years_available = [2019, 2020, 2021]
granularity = ['county', 'state']

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
        params = request.GET.dict() or request.POST.dict()
        path = request.path
        event = request.method
        new_record = Transaction(
            event=event, path=path, params=params, status_code=status_code)
        new_record.save()
    except Exception as e:
        raise e
    

def logger(func):
    def wrapper(request: HttpRequest):
        try:
            response = func(request)
            status_code = response.status_code
            log_event(request, status_code)
            return response
        except Exception as e:
            raise e
    return wrapper


@logger
def index(request: HttpRequest):
    return render(request, 'index.html', {
        'title': 'Head Start Annual Statistics',
        'years_select': years_available,
        'granularity_select': granularity,
    })


@logger
def view(request: HttpRequest):
    try:
        params = request.GET.dict()
        gra = params['granularity']
        year = int(params['year'])
        if gra == 'state':
            data = data_factory.get_state_data(year)
            data = data[['state', 'enroll_rate']]
            data = data.sort_values(
                by='enroll_rate', ascending=False).head(5).values
            vis_config = json.dumps({
                'title': 'Top 5 States with Highest Enroll Rate',
                'data': data.tolist()
                }, 
                cls=CustomJSONEncoder
            )
        elif gra == 'county':
            data = data_factory.get_county_data(year)
            data = data[['state_county', 'cpc', ]]
            data = data.sort_values(by='cpc', ascending=False).head(5).values
            vis_config = json.dumps({
                'title': 'Top 5 Counties with Highest Estimated Children per Center',
                'data': data.tolist()
            }, 
                cls=CustomJSONEncoder
            )
        else:
            raise Exception('Invalid granularity')

        return render(request, 'view.html', {
            'title': 'Head Start Annual Statistics',
            'years_select': years_available,
            'granularity_select': granularity,
            'year': year,
            'granularity': gra,
            'data': data,
            'vis_config': vis_config,
        })

    except Exception as e:
        raise e
