"""
App for get the current weather and forecast data for the given location.

@Arguments
    Positionals and required
        command : current or forecast
        locations: in "{city},{country code}" format.
    Optionals:
        --units (metric or imperial)
        --days (integer between 1 and 5)


Examples:
myweatherapp current Irvine,US --units=imperial
myweatherapp forecast Santander,ES --days=3

"""

from dataclasses import dataclass
from typing import List
from data_api_accuweather import DataAPIAccuweather
from constant import Const
from data_api_weather import DataAPIWeather
from data_input import DataInput
from data_view import DataView


@dataclass
class MyWeatherAPP():
    '''
    Main class
    '''
    data_input: DataInput
    data_source: DataAPIWeather
    data_view: List[DataView]

    def get_current_weather(self):
        '''
        get_current_weather
        '''
        self.data_view = self.data_source.current_weather(
            self.data_input.units)

    def get_forecast_weather(self):
        '''
        get forecast weather
        '''
        self.data_view = self.data_source.forecast_weather(
            self.data_input.units, self.data_input.days)

    def show_output(self):
        '''
        show results in console
        '''
        for data in self.data_view:
            data.show_console()


def main():
    '''
    main function
    '''
    data_input = DataInput()
    data_input.get_arguments()
    accuweather = DataAPIAccuweather(data_input.city, data_input.country)
    print(f"{data_input.city} ({data_input.country})\n")
    app = MyWeatherAPP(data_input, accuweather, [])
    if app.data_input.command == Const.CURRENT:
        app.get_current_weather()
    if data_input.command == Const.FORECAST:
        app.get_forecast_weather()
    if app.data_view:
        app.show_output()


if __name__ == '__main__':
    main()
