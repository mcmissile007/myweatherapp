'''
comments
'''

from dataclasses import dataclass, field
import json
from typing import List
from http_request import HttpRequest
from data_api_weather import DataAPIWeather
from private.config import AccuweatherPrivate
from constant import Const
from data_view import DataView


@dataclass
class DataAPIAccuweather(DataAPIWeather):
    '''
    class for access AccuWeather API
    '''
    city: str
    country_code: str
    _location_key: str = field(init=False, default="", repr=False)
    _api_version: str = field(init=False, default="v1", repr=False)
    _api_key: str = AccuweatherPrivate.API_KEY
    _base_url: str = field(
        init=False, default="http://dataservice.accuweather.com", repr=False)

    def __post_init__(self) -> None:
        '''
        initialize self._location_key for the city and country_code
        if api call fail self._location_key = ""
        '''
        self._get_location_key()

    @staticmethod
    def _parse_current_weather(response: str, units: str) -> List[DataView]:
        '''
        get a summary (date, text and temperature) dict from current weather conditions api response
        @param response: http_response from API call
        @param days: number of  days to retrieve forecast data for
        @return: a dict with date, text and temperature fields
        '''
        dataviews = []

        try:
            data_view = DataView()
            conditions = json.loads(response)[0]
            data_view.text = conditions["WeatherText"]
            data_view.date = conditions["LocalObservationDateTime"].split("T")[0]
            if units == Const.METRIC:
                data_view.temperature = conditions["Temperature"]["Metric"]["Value"]
                data_view.units= conditions["Temperature"]["Metric"]["Unit"]
            if units == Const.IMPERIAL:
                data_view.temperature = conditions["Temperature"]["Imperial"]["Value"]
                data_view.units = conditions["Temperature"]["Imperial"]["Unit"]
            dataviews.append(data_view)
        except json.JSONDecodeError as json_errror:
            print(f"{json_errror}")
        except KeyError as key_error:
            print(f"{key_error}")

        return dataviews

    @staticmethod
    def _parse_forecast_weather(response: str, days: int) -> List[DataView]:
        '''
        get a summary (date, text and temperature) from forecast api response
        @param response: http_response from API call
        @param days: number of  days to retrieve forecast data for
        @return: a list of dataview objects
        '''
        dataviews = []

        try:
            for forecast in json.loads(response)["DailyForecasts"][:days]:
                data_view = DataView()
                data_view.date = forecast["Date"].split("T")[0]
                data_view.text= forecast["Day"]["LongPhrase"]
                data_view.temperature = forecast["Temperature"]["Maximum"]["Value"]
                data_view.units= forecast["Temperature"]["Maximum"]["Unit"]
                dataviews.append(data_view)
        except json.JSONDecodeError as json_errror:
            print(f"{json_errror}")
        except KeyError as key_error:
            print(f"{key_error}")

        return dataviews

    @staticmethod
    def _parse_location_response(response: str) -> str:
        '''
        get the location_key to use in accweather api calls
        @param response: http_response from location API call
        @return: the location_key or "" if error
        '''
        try:
            locations = json.loads(response)
            if locations and "Key" in locations[0]:
                return locations[0]['Key']
        except json.JSONDecodeError as json_errror:
            print(f"{json_errror}")
        return ""


    def _get_location_key(self) -> None:
        '''
        set self._location_key based on instance properties city and country_code
        if api call faile self._location_key = ""
        '''
        url = f"{self._base_url}/locations/{self._api_version}/cities/{self.country_code}/search"
        query = {"apikey": self._api_key, "q": self.city}
        response = HttpRequest().simple_http_request(url, query)
        if response:
            self._location_key = DataAPIAccuweather._parse_location_response(
                response)



    def current_weather(self, units: str) -> List[DataView]:
        """
        return the  current weather conditions
        @param: units for temperature : metric or imperial
        @return: a list of Dataview objects
        """
        url = f"{self._base_url}/currentconditions/{self._api_version}/{self._location_key}"
        query = {"apikey": self._api_key}
        response = HttpRequest().simple_http_request(url, query)
        if response:
            return DataAPIAccuweather._parse_current_weather(
                response, units)
        print("No data available")
        return []

    def forecast_weather(self, units: str, days: int) -> List[DataView]:
        """
        return the forecast weather conditions
        @param: units for temperature (metric or imperial)
        @param: days: days to retrieve forecast data for
        @return: a list of Dataview objects
        """
        url = f"{self._base_url}/forecasts/{self._api_version}/daily/5day/{self._location_key}"

        query = {"apikey": self._api_key, "details": "true"}
        if units == Const.METRIC:
            query["metric"] = "true"
        response = HttpRequest().simple_http_request(url, query)
        if response:
            return DataAPIAccuweather._parse_forecast_weather(
                response, days)
        print("No data available")
        return []
