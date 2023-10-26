from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .data import DataFactory

years_available = [2019, 2020, 2021]
granularity = ['county', 'state']
data_factory = DataFactory()


def index(request: HttpRequest):
    return render(request, 'index.html', {
        'title': 'Head Start Annual Statistics',
        'years_select': years_available,
        'granularity_select': granularity,
    })


def view(request: HttpRequest):
    try:
        params = request.GET.dict()
        gra = params['granularity']
        year = int(params['year'])
        if gra == 'state':
            data = data_factory.get_state_data(year)
            data = data[['state', 'child_poverty_count', 'federal_funding',
                         'enroll_count', 'personal_income', 'fund_per_child', 'enroll_rate']]
            data = data.sort_values(
                by='enroll_rate', ascending=False).head(5).values
        elif gra == 'county':
            data = data_factory.get_county_data(year)
            data = data[['state', 'county', 'cpc', ]]
            data = data.sort_values(by='cpc', ascending=False).head(5).values
        else:
            raise Exception('Invalid granularity')

        return render(request, 'view.html', {
            'title': 'Head Start Annual Statistics',
            'years_select': years_available,
            'granularity_select': granularity,
            'year': year,
            'granularity': gra,
            'data': data,
        })

    except Exception as e:
        raise e


def child_per_center(request: HttpRequest):
    try:
        params = request.GET
        gra = params['granularity']
        year = int(params['year'])
        return render(request, 'child_per_center.html', {
            'title': 'Children per Center',
            'value': 21312
        })
    except:
        raise
