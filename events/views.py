import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from csos.models import RiverCso, RiverOutfall
from events.analyzer import rainfall_graph, find_n_years
from events.models import HourlyPrecip
from flooding.models import BasementFloodingEvent


def index(request):
    _default_start = '2011-07-22 22:00:00'
    _default_end = '2011-07-23 10:00:00'
    return show_date(request, _default_start, _default_end)


def show_date(request, start_stamp, end_stamp):
    ret_val = {}

    try:
        start = pd.to_datetime(start_stamp)
        end = pd.to_datetime(end_stamp)

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
            ret_val['high_intensity'] = "%s inches in %s hours.  A %s-year storm" % (
                high_intensity['inches'], high_intensity['duration_hrs'], high_intensity['n'])

        graph_data = {'total_rainfall_data': rainfall_graph(hourly_precip_df)}

        csos_db = RiverCso.objects.filter(open_time__range=(start, end)).values() | RiverCso.objects.filter(
            close_time__range=(start, end)).values()

        csos_df = pd.DataFrame(list(csos_db))

        csos = []
        ret_val['sewage_river'] = 'None'

        if len(csos_df) > 0:

            csos_df['duration'] = (csos_df['close_time'] - csos_df['open_time'])
            ret_val['sewage_river'] = "%s minutes" % int(csos_df['duration'].sum().seconds / 60)

            river_outfall_ids = csos_df['river_outfall_id'].unique()
            river_outfall_ids = list(river_outfall_ids)
            river_outfalls = RiverOutfall.objects.filter(
                id__in=river_outfall_ids,
                lat__isnull=False
            )

            for river_outfall in river_outfalls:
                csos.append({'lat': river_outfall.lat, 'lon': river_outfall.lon})

        cso_map = {'cso_points': csos}
        graph_data['cso_map'] = cso_map

        flooding_df = pd.DataFrame(
            list(BasementFloodingEvent.objects.filter(date__gte=start).filter(date__lte=end).values()))

        flooding_df = flooding_df.drop('id', 1).groupby(['unit_id', 'unit_type']).sum()
        flooding_df.columns = ['value']
        flooding_df['unit_type'] = flooding_df.index.get_level_values('unit_type')
        flooding_df['label'] = flooding_df.index.get_level_values('unit_id')
        flooding = {'wards': flooding_df[flooding_df['unit_type'] == 'ward'].drop('unit_type', 1).to_dict('record'),
                    'community': flooding_df[flooding_df['unit_type'] == 'community'].drop('unit_type', 1).to_dict(
                        'record'),
                    'zip': flooding_df[flooding_df['unit_type'] == 'zip'].drop('unit_type', 1).to_dict('record'),
                    }
        graph_data['flooding_data'] = flooding
        ret_val['basement_flooding'] = flooding_df[flooding_df['unit_type'] == 'ward']['value'].sum()
        ret_val['graph_data'] = graph_data

    except ValueError as e:
        return HttpResponse("Not valid dates")

    ret_val['hourly_precip'] = str(hourly_precip_df.head())
    return render(request, 'show_event.html', ret_val)
