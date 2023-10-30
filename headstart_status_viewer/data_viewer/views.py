from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .dataPipeline import data_factory
from .models import Transaction
import json
from .utils import CustomJSONEncoder
from datetime import datetime
from .customExceptions import DataNotFoundError, DataFormatError


def get_available_years():
    year_now = datetime.now().year
    return list(range(2019, year_now + 1))

granularity_available = ['county', 'state']
        


def log_event(request: HttpRequest, status_code: int):
    try:
        ip = request.META.get('REMOTE_ADDR')
        params = request.GET.dict() or request.POST.dict()
        path = request.path
        met = request.method
        new_record = Transaction(ip = ip, method=met, path=path, params=params, status_code=status_code)
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


@logger
def index(request: HttpRequest):
    return render(request, 'index.html', {
        'title': 'Head Start Annual Statistics',
        'years_select': get_available_years(),
        'granularity_select': granularity_available,
    })


@logger
def view(request: HttpRequest):
    try:
        params = request.GET.dict()
        selected_granularity = params['granularity']
        year = int(params['year'])
        if selected_granularity == 'state':
            data = data_factory.get_state_data(year)
            data = data[['state', 'fund_per_child', 'rgdp', 'enrollment_rate']]
            data = data.sort_values(by='enrollment_rate', ascending=False).head(5).values
            vis_config = json.dumps({
                'title': 'Top 5 States with Highest Enroll Rate',
                'data': data.tolist()
                }, 
                cls=CustomJSONEncoder
            )
        elif selected_granularity == 'county':
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
            raise DataFormatError('Invalid granularity')

        return render(request, 'view.html', {
            'title': 'Head Start Annual Statistics',
            'years_select': get_available_years(),
            'granularity_select': granularity_available,
            'year': year,
            'granularity': selected_granularity ,
            'data': data,
            'vis_config': vis_config,
        })
    
    except DataNotFoundError as e:
        return redirect('error',)

    except DataFormatError as e:
        return redirect('error',)
    
    except Exception as e:
        raise e


@logger
def error(request: HttpRequest):

    return render(request, 'error.html', {
        'title': 'Head Start Annual Statistics',
    })