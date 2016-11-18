import operator
import os
from datetime import timedelta

import pandas as pd
from csos.models import RiverOutfall, RiverCso
from rainapp.settings import BASE_DIR
import numpy as np


def rainfall_graph(hourly_precip_df):
    time_list = list(hourly_precip_df['start_time'].apply(lambda x: x.strftime("%d/%m %H:%M")))
    hourly_rainfall = list(hourly_precip_df['precip'])
    cumulative_rain = list(hourly_precip_df['precip'].cumsum())

    return {'time_list': time_list, 'hourly_rainfall': hourly_rainfall, 'cumulative_rain': cumulative_rain}


def find_n_years(hourly_precip_df):
    thresh_dir = os.path.join(BASE_DIR, 'events', 'raw_data', 'n_year_definitions.csv')
    n_year_threshes = pd.read_csv(thresh_dir)
    n_year_threshes = n_year_threshes.set_index('Duration')
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
    n_s = [int(x.replace('-year', '')) for x in reversed(list(n_year_threshes.columns.values))]
    duration_strs = sorted(dur_str_to_hours.items(), key=operator.itemgetter(1), reverse=False)
    rain_series = hourly_precip_df[['end_time', 'precip']].set_index('end_time')
    for n in n_s:
        n_index = n_s.index(n)
        next_n = n_s[n_index - 1] if n_index != 0 else None
        for duration_tuple in duration_strs:

            duration_str = duration_tuple[0]
            low_thresh = n_year_threshes.loc[duration_str, str(n) + '-year']
            high_thresh = n_year_threshes.loc[duration_str, str(next_n) + '-year'] if next_n is not None else None

            duration = int(dur_str_to_hours[duration_str])
            rolling = rain_series['precip'].rolling(window=int(duration), min_periods=0).sum()

            if high_thresh is not None:
                event_endtimes = rolling[(rolling >= low_thresh) & (rolling < high_thresh)].sort_values(ascending=False)
            else:
                event_endtimes = rolling[(rolling >= low_thresh)].sort_values(ascending=False)
            if len(event_endtimes) > 0:
                event = event_endtimes[0:1]

                return {'n': n, 'end_time': event.index, 'inches': event[0],
                        'duration_hrs': duration,
                        'start_time': pd.to_datetime(event.index) - timedelta(hours=duration)}
    return None


def build_flooding_data(flooding_df):
    flooding_df = flooding_df.drop('id', 1).groupby(['unit_id', 'unit_type']).sum()
    flooding_df['unit_type'] = flooding_df.index.get_level_values('unit_type')
    flooding_df['label'] = flooding_df.index.get_level_values('unit_id')

    flooding_data = {'community': flooding_df[flooding_df['unit_type'] == 'community'].sort_values(
        'label').to_dict("record")}
    flooding_df = flooding_df[flooding_df['unit_type'] != 'community']
    flooding_df['label'] = flooding_df['label'].apply(lambda x: int(x))
    flooding_data['wards'] = flooding_df[flooding_df['unit_type'] == 'ward'].sort_values('label').to_dict("record")
    flooding_data['zip'] = flooding_df[flooding_df['unit_type'] == 'zip'].sort_values('label').to_dict("record")

    return flooding_data


def build_csos(start, end):
    cso_events = RiverCso.objects.filter(open_time__range=(start, end)).values() | RiverCso.objects.filter(
        close_time__range=(start, end)).values() | RiverCso.objects.filter(open_time__lte=start).filter(
        close_time__gte=end).values()

    cso_outfall_events = {ro['id']: ro for ro in RiverOutfall.objects.all().values()}
    durations = []

    for cso_event in cso_events:
        river_outfall_id = cso_event['river_outfall_id']
        duration = (cso_event['close_time'] - cso_event['open_time']).total_seconds() / 60
        if "minutes" not in cso_outfall_events[river_outfall_id]:
            cso_outfall_events[river_outfall_id]['minutes'] = 0
        cso_outfall_events[river_outfall_id]['minutes'] += duration
        durations.append(duration)
        if "popup" not in cso_outfall_events[river_outfall_id]:
            cso_outfall_events[river_outfall_id]['popup'] = ""
        cso_outfall_events[river_outfall_id]['popup'] += cso_event['open_time'].strftime('%m/%d %H:%M') + '-' + \
                                                         cso_event['close_time'].strftime('%m/%d %H:%M') + '<BR>'

    durations.sort()
    # durations_split = np.split(durations, 4)

    percentiles = {25: np.percentile(durations, 25), 50: np.percentile(durations, 50), 75: np.percentile(durations, 75)}

    cso_points = []
    for coe_id in cso_outfall_events:
        cso_outfall_event = cso_outfall_events[coe_id]
        if "minutes" not in cso_outfall_event:  # Skip outfall points without an overflow
            continue
        if cso_outfall_event['minutes'] < percentiles[25]:
            cso_outfall_event['color'] = 'blue'
        elif cso_outfall_event['minutes'] <= percentiles[50]:
            cso_outfall_event['color'] = 'green'
        elif cso_outfall_event['minutes'] <= percentiles[75]:
            cso_outfall_event['color'] = 'orange'
        else:
            cso_outfall_event['color'] = 'red'

        cso_outfall_event['radius'] = 300
        cso_outfall_event['popup'] = cso_outfall_event['name'] + '<br>' + "Minutes: " + str(
            int(cso_outfall_event['minutes'])) + '<br>' + cso_outfall_event['popup']
        cso_points.append(cso_outfall_event)

    return cso_points
