import os

import sqlite3
from django.core.management.base import BaseCommand

from csos.models import RiverOutfall
from rainapp.settings import BASE_DIR

import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):

        flooding_list = []
        data_dir = os.path.join(BASE_DIR, 'events', 'raw_data')

        wib_by_ward = pd.read_csv(os.path.join(data_dir, 'wib_calls_311_ward.csv'))
        wib_by_ward = wib_by_ward.set_index("Created Date")
        for index, row in wib_by_ward.iterrows():
            for ward_number in wib_by_ward.columns:
                flooding_list.append({'date': index, 'count': row[ward_number], 'unit_type': 'ward',
                                      'unit_id': ward_number})

        wib_by_comm = pd.read_csv(os.path.join(data_dir, 'wib_calls_311_comm.csv'))
        wib_by_comm = wib_by_comm.set_index("Created Date")
        for index, row in wib_by_comm.iterrows():
            for neigh in wib_by_comm.columns:
                flooding_list.append({'date': index, 'count': row[neigh], 'unit_type': 'community',
                                      'unit_id': neigh.title()})

        wib_by_zip = pd.read_csv(os.path.join(data_dir, 'wib_calls_311_zip.csv'))
        wib_by_zip = wib_by_zip.set_index("Created Date")
        for index, row in wib_by_zip.iterrows():
            for zip_code in wib_by_zip.columns:
                flooding_list.append({'date': index, 'count': row[zip_code], 'unit_type': 'zip',
                                      'unit_id': zip_code})

        flooding = pd.DataFrame(flooding_list)
        flooding = flooding[flooding['count'] > 0]
        print(len(flooding))

        db_dir = os.path.join(BASE_DIR, 'db.sqlite3')
        cnx = sqlite3.connect(db_dir)
        # flooding.to_sql('flooding_basementfloodingevent', cnx, if_exists='append', index_label='id')
