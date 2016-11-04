import os

import sqlite3
from django.core.management.base import BaseCommand

from csos.models import LakeOutfall
from rainapp.settings import BASE_DIR

import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **options):

        lake_outfalls = {ro.name: ro for ro in LakeOutfall.objects.all()}

        reversal_file = os.path.join(BASE_DIR, 'events', 'raw_data', 'lake_michigan_reversals.csv')
        reversals = pd.read_csv(reversal_file)
        reversals['start_date'] = pd.to_datetime(reversals['start_date'])
        reversals.loc[reversals['end_date'].isnull(), 'end_date'] = reversals[reversals['end_date'].isnull()][
            'start_date']

        reversals['end_date'] = pd.to_datetime(reversals['end_date'])

        lake_reversals = []
        for index, reversal in reversals.iterrows():
            for plant in ['crcw', 'obrien', 'wilmette']:
                if reversal[plant] > 0:
                    lake_reversals.append(
                        {'lake_outfall_id': lake_outfalls[plant].id, 'open_date': reversal['start_date'],
                         'close_date': reversal['end_date'], 'millions_of_gallons': reversal[plant]})
        lake_reversals = pd.DataFrame(lake_reversals)
        db_dir = os.path.join(BASE_DIR, 'db.sqlite3')
        cnx = sqlite3.connect(db_dir)
        lake_reversals.to_sql('csos_lakereversal', cnx, if_exists='append', index_label='id')
