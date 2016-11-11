import pandas as pd
from django.shortcuts import render

from csos.models import LakeOutfall, LakeReversal


def index(request):
    return reversals(request)


def reversals(request):
    lake_outfalls = {lo.id: lo.name for lo in LakeOutfall.objects.all()}

    lake_reversals = pd.DataFrame(list(LakeReversal.objects.all().values()))
    total_sewage = lake_reversals['millions_of_gallons'].sum()
    lake_reversals['year'] = lake_reversals['open_date'].apply(lambda x: x.year)
    lake_reversals['lake_outfall_id'] = lake_reversals['lake_outfall_id'].apply(lambda x: lake_outfalls[x])
    lake_reversals = lake_reversals.drop(['close_date', 'open_date'], 1)
    lake_reversals = lake_reversals.groupby(['lake_outfall_id', 'year']).sum()
    lake_reversals = lake_reversals.transpose()

    values = {name: [] for name in lake_outfalls.values()}
    years = []
    for year in reversed(range(1985, 2017)):
        years.append(year)
        for station in lake_outfalls.values():
            values[station].append(lake_reversals[station][year]['millions_of_gallons'] if year in lake_reversals[station] else 0)
    ret_val = {'total_sewage': total_sewage * 1000000,
               'events': {'years': years,
                          'series': [{'name': 'Downtown', 'data': values['crcw']},
                                     {'name': 'Calumet', 'data': values['obrien']},
                                     {'name': 'Wilmette', 'data': values['wilmette']}]
                          }}

    return render(request, 'lake_reversals.html', ret_val)
