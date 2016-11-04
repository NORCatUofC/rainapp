def rainfall_graph(hourly_precip_df):
    time_list = list(hourly_precip_df['start_time'].apply(lambda x: x.strftime("%d/%m %H:%M")))
    hourly_rainfall = list(hourly_precip_df['precip'])
    cumulative_rain = list(hourly_precip_df['precip'].cumsum())

    # TODO: Create the variables for the total rainfall graph

    # These are the attributes of hourly_precip_df
    # start_time = models.DateTimeField()
    # end_time = models.DateTimeField()
    # precip = models.FloatField()
    return {'time_list': time_list, 'hourly_rainfall': hourly_rainfall, 'cumulative_rain': cumulative_rain}
