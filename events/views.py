import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from events.analyzer import rainfall_graph
from events.models import HourlyPrecip


def index(request):
    return HttpResponse("Under Construction")


def show_date(request, start_stamp, end_stamp):
    ret_val = {}

    try:
        start = pd.to_datetime(start_stamp)
        end = pd.to_datetime(end_stamp)

        hp = HourlyPrecip.objects.filter(
            start_time__gte=start,
            end_time__lte=end
        ).values()
        hourly_precip_dict = list(hp)
        hourly_precip_df = pd.DataFrame(hourly_precip_dict)

        ret_val['total_rainfall'] = hourly_precip_df['precip'].sum()

        ret_val['rainfall_graph'] = rainfall_graph(hourly_precip_df)

    except ValueError:
        return HttpResponse("Not valid dates")

    ret_val['hourly_precip'] = str(hourly_precip_df.head())
    return render(request, 'show_event.html', ret_val)
