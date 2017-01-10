# import the Open Weather Map API Python wrapper/library
import pyowm

weather_info = pyowm.OWM('9f5a070c55d4e730d6cbc3bb93e3a186')


def weather_query(location):
    current_weather = weather_info.weather_around_coords(location[1], location[2]).get_weather()

    # current_weather.get_rain()
    # current_weather.get_snow()
    # current_weather.get_temperature
    # etc
