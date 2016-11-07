import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from csos.models import RiverCso, RiverOutfall
from events.analyzer import rainfall_graph, find_n_years
from events.models import HourlyPrecip


def index(request):
    return HttpResponse("Under Construction")


def show_date(request, start_stamp, end_stamp):
    ret_val = {}

    try:
        start = pd.to_datetime(start_stamp)
        end = pd.to_datetime(end_stamp)

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

        csos_df = pd.DataFrame(
            list(
                RiverCso.objects.filter(
                    open_time__gte=start,
                    close_time__lte=end
                ).values()
            )
        )

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

        ret_val['graph_data'] = graph_data

    except ValueError:
        return HttpResponse("Not valid dates")

    ret_val['hourly_precip'] = str(hourly_precip_df.head())
    return render(request, 'show_event.html', ret_val)
