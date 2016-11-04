import os

import sqlite3
from django.core.management.base import BaseCommand
from rainapp.settings import BASE_DIR
from datetime import timedelta

import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Hourly precipitation data is not available in the repo because it is too large
        precip_file_name = os.path.join(BASE_DIR, 'events', 'raw_data', 'ohare_hourly_20160929.csv')
        rain_df = pd.read_csv(precip_file_name)
        rain_df['datetime'] = pd.to_datetime(rain_df['datetime'])
        rain_df = rain_df.set_index(pd.DatetimeIndex(rain_df['datetime']))
        rain_df = rain_df['19700101':]
        chi_rain_series = rain_df['HOURLYPrecip'].resample('1H', label='right').max().fillna(0)
        hourly_precip = pd.DataFrame(chi_rain_series)
        hourly_precip.columns = ['precip']
        hourly_precip['end_time'] = pd.to_datetime(hourly_precip.index.values)
        hourly_precip['start_time'] = hourly_precip['end_time'] - timedelta(hours=1)
        hourly_precip.index = range(len(hourly_precip))
        db_dir = os.path.join(BASE_DIR, 'db.sqlite3')
        cnx = sqlite3.connect(db_dir)
        hourly_precip.to_sql('events_hourlyprecip', cnx, if_exists='append', index_label='id')
