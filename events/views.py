import os

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from events.analyzer import rainfall_graph, find_n_years, build_flooding_data, build_cso_map
from events.models import HourlyPrecip, NYearEvent
from flooding.models import BasementFloodingEvent
from rainapp.settings import BASE_DIR


def index(request):
    _default_start = '07/22/2011 08:00'
    _default_end = '07/23/2011 06:00'
    return show_date(request, _default_start, _default_end)


def show_date(request, start_stamp, end_stamp):
    ret_val = {}

    try:
        start = pd.to_datetime(start_stamp)
        end = pd.to_datetime(end_stamp)

        if start > end:
            return HttpResponse("Start time must before end time")

        if (end - start).days > 10:
            return HttpResponse("Search only on 10 day periods")

    except:
        return HttpResponse("Not valid dates")

    try:

        ret_val['start_date'] = start.strftime("%m/%d/%Y %H:%M")
        ret_val['end_date'] = end.strftime("%m/%d/%Y %H:%M")

        hourly_precip_dict = list(
            HourlyPrecip.objects.filter(
                start_time__gte=start,
                end_time__lte=end
            ).values()
        )
        hourly_precip_df = pd.DataFrame(hourly_precip_dict)

        ret_val['total_rainfall'] = "%s inches" % hourly_precip_df['precip'].sum()

        high_intensity = find_n_years(hourly_precip_df)
        if high_intensity is None:
            ret_val['high_intensity'] = 'No'
        else:
            ret_val['high_intensity'] = "%s inches in %s hours!<br>  A %s-year storm" % (
                high_intensity['inches'], high_intensity['duration_hrs'], high_intensity['n'])

        graph_data = {'total_rainfall_data': rainfall_graph(hourly_precip_df)}

        ret_val['sewage_river'] = 'None'

        ret_val['cso_map'] = build_cso_map(start, end)

        flooding_df = pd.DataFrame(
            list(BasementFloodingEvent.objects.filter(date__gte=start).filter(date__lte=end).values()))

        if len(flooding_df) > 0:
            graph_data['flooding_data'] = build_flooding_data(flooding_df)
            ret_val['basement_flooding'] = flooding_df[flooding_df['unit_type'] == 'ward']['count'].sum()
        else:
            graph_data['flooding_data'] = {}
            ret_val['basement_flooding'] = 0
        ret_val['graph_data'] = graph_data

    except Exception as e:
        return HttpResponse("Boom: ")

    ret_val['hourly_precip'] = str(hourly_precip_df.head())
    return render(request, 'show_event.html', ret_val)


def viz_animation(request):
    return render(request, 'viz.html')


def basement_flooding(request):
    return render(request, 'flooding.html')


def viz_splash(request):
    return render(request, 'viz-splash.html')


def about(request):
    return render(request, 'about.html')


def nyear(request):
    events_db = NYearEvent.objects.all()
    storm_intervals = [1, 2, 5, 10, 25, 50, 100]
    events = {n: [] for n in storm_intervals}
    for event in events_db:
        date_formatted = event.start_time.strftime("%m/%d/%Y") + "-" + event.end_time.strftime("%m/%d/%Y")
        duration = str(event.duration_hours) + ' hours' if event.duration_hours <= 24 else str(
            int(event.duration_hours / 24)) + ' days'
        events[event.n].append({'date_formatted': date_formatted, 'inches': "%.2f" % event.inches,
                                'duration_formatted': duration,
                                'event_url': '/date/%s/%s' % (event.start_time, event.end_time)})

    thresh_dir = os.path.join(BASE_DIR, 'events', 'raw_data', 'n_year_definitions.csv')
    n_year_threshes = pd.read_csv(thresh_dir)

    dur_str_to_hours = {
        '1-hr': 1.0,
        '2-hr': 2.0,
        '3-hr': 3.0,
        '6-hr': 6.0,
        '12-hr': 12.0,
        '18-hr': 18.0,
        '24-hr': 24.0,
        '48-hr': 48.0,
        '72-hr': 72.0,
        '5-day': 5 * 24.0,
        '10-day': 10 * 24.0
    }

    n_year_threshes['Duration'] = n_year_threshes['Duration'].apply(lambda x: str(int(dur_str_to_hours[x])))
    n_year_threshes = n_year_threshes.set_index('Duration')

    n_year_thresholds = {'durations': list(n_year_threshes.index.values),
                         'boundaries': n_year_threshes.to_dict('dict'),
                         'recurrence_intervals': list(n_year_threshes.columns)}

    return render(request, 'nyear.html', {'nyear_events': events, 'storm_intervals': storm_intervals,
                                          'n_year_thresholds': n_year_thresholds})
