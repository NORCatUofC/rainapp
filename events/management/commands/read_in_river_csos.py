import os

import sqlite3
from django.core.management.base import BaseCommand

from csos.models import RiverOutfall
from rainapp.settings import BASE_DIR

import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):

        river_outfalls = {ro.name: ro for ro in RiverOutfall.objects.all()}

        cso_file = os.path.join(BASE_DIR, 'events', 'raw_data', 'merged_cso_data.csv')
        csos = pd.read_csv(cso_file)
        csos = csos[['Outfall Structure', 'Open date/time', 'Close date/time']]
        csos.columns = ['outfall', 'open_time', 'close_time']
        for index, cso in csos.iterrows():
            if cso['outfall'] in river_outfalls:
                csos.loc[index, 'river_outfall_id'] = river_outfalls[cso['outfall']].id
            else:
                csos.loc[index, 'river_outfall_id'] = river_outfalls['unknown'].id
        csos = csos.drop('outfall', 1)
        db_dir = os.path.join(BASE_DIR, 'db.sqlite3')
        cnx = sqlite3.connect(db_dir)
        csos.to_sql('csos_rivercso', cnx, if_exists='append', index_label='id')
