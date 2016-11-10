import os
import sqlite3
from django.core.management.base import BaseCommand
from rainapp.settings import BASE_DIR

import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **options):

        nyear_file = os.path.join(BASE_DIR, 'events', 'raw_data', 'n_year_storms_ohare_noaa.csv')
        nyears = pd.read_csv(nyear_file)
        nyears = nyears.rename(columns={'duration_hrs': 'duration_hours'}).drop('year', 1)

        db_dir = os.path.join(BASE_DIR, 'db.sqlite3')
        cnx = sqlite3.connect(db_dir)
        # nyears.to_sql('events_nyearevent', cnx, if_exists='append', index_label='id')
