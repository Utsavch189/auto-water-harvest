import requests
from decouple import config
from datetime import datetime,timedelta

class WeatherApi:

    def __init__(self,latitude,longitude):
        self.latitude=latitude
        self.longitude=longitude

    def getTodayWeatherForecast(self):
        params = {
            'lat': self.latitude,
            'lon': self.longitude,
            'appid': config('API_KEY'),
            'units': 'metric',
            'exclude': config('EXCLUDE')
        }
        currentWeather_api_address=f'http://api.openweathermap.org/data/2.5/onecall'
        res=requests.get(currentWeather_api_address,params=params).json()

        try:
            if 'hourly' in res:
                current_time = datetime.now()
                one_hour_later = current_time + timedelta(hours=1)

                for hourly_data in res['hourly']:
                    forecast_time = datetime.fromtimestamp(hourly_data['dt'])
                    if forecast_time.hour == one_hour_later.hour:
                        return hourly_data
            else:
                return "No Forecast..."

        except Exception as e:
            raise Exception(str(e))

# w=WeatherApi(
#     latitude=23.205502,
#     longitude=88.404976
# )
# w.getTodayWeatherForecast()