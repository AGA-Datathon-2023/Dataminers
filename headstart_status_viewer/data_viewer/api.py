from django.http import HttpRequest, HttpResponse, FileResponse
from .dataPipeline import data_factory
import io

class API:
    @staticmethod
    def download(request: HttpRequest) -> HttpResponse:
        try:
            params = request.GET.dict()
            gra = params['granularity']
            year = int(params['year'])
            with io.StringIO() as io_obj:
                if gra == 'state':
                    data = data_factory.get_state_data(year)
                    data.to_csv(io_obj)
                elif gra == 'county':
                    data = data_factory.get_county_data(year)
                    data.to_csv(io_obj)
                else:
                    raise Exception('Invalid granularity')
                content = io_obj.getvalue()
            resp = FileResponse(content, content_type='text/csv', filename='data.csv', as_attachment=True)
            return resp
        except:
            pass