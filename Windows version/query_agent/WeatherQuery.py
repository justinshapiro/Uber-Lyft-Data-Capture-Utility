# import the Open Weather Map API Python wrapper/library
import pyowm

# import querying framework
from AgentQueryFramework import *

weather_info = pyowm.OWM('9f5a070c55d4e730d6cbc3bb93e3a186')


# Get the weather for a location
def weather_query(location):
    # get the weather from an Observation object
    current_weather = weather_info.weather_around_coords(location[1], location[2], limit=1)[0].get_weather()

    # get and parse the average of the high and low temperatures recorded
    temp = current_weather.get_temperature(unit='fahrenheit')
    if str(temp) != "None":
        temp = str(clean(json_parse(temp, "temp")))
    else:
        temp = ""

    # get the rainfall in mm during the last 3 hours
    rain = current_weather.get_rain()
    if str(rain) != "{}":
        rain = str(clean(str(rain).split(':', 1)[-1]))
    else:
        rain = ""

    # get the snowfall in mm during the last 3 hours
    snow = current_weather.get_snow()
    if str(snow) != "{}":
        snow = str(clean(str(snow).split(':', 1)[-1]))
    else:
        snow = ""

    return [temp, rain, snow]

