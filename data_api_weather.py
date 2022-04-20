"""
comments
"""

from abc import ABC, abstractmethod
from typing import List
from data_view import DataView


class DataAPIWeather(ABC):
    """
    Abstract class for future data sources
    """
    city: str
    country_code: str

    @abstractmethod
    def current_weather(self, units: str) -> List[DataView]:
        """
        show in the console the  current weather conditions
        @param units for temperature : metric or imperial
        @return a list of DataView objects
        """

    @abstractmethod
    def forecast_weather(self, units: str, days: int) -> List[DataView]:
        """
        show in the console the forecast weather conditions
        @param: units for temperature (metric or imperial)
        @param: days: days to retrieve forecast data for
        @return: a list of Dataview objects
        """
