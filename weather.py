import pyowm

class Weather(object):
    def __init__(self):
        _owm = pyowm.OWM('eabd5dadca1b362ea8820525ffccd652')
    def current_weather(self, place):
        try:
            obs = _owm.weather_at_place(place)
        except:
            try:
                obs = owm.weather_at_id(int(place)) 
            except:
                try:
                    obs = owm.weather_at_coords(place)
                except:
                    return "Cannot find %s." %(place)
        return obs
if __name__ == '__main__':
    oWeather = Weather()
    output = oWeather.current_weather('London, UK')
    print output


