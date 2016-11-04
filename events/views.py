import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from events.models import HourlyPrecip


def index(request):
    return HttpResponse("Under Construction")


def show_date(request, start_stamp, end_stamp):
    data = {}

    try:
        start = pd.to_datetime(start_stamp)
        end = pd.to_datetime(end_stamp)

        hp = list(HourlyPrecip.objects.filter(
            start_time__gte=start,
            end_time__lte=end
        ))

        hourly_precip = pd.DataFrame(hp)

    except ValueError:
        return HttpResponse("Not valid dates")



    data['hourly_precip'] = str(hourly_precip.head())
    return render(request, 'show_event.html', data)