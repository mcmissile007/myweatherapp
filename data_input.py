'''
comments
'''
from dataclasses import dataclass, field

import argparse

from constant import Const


@dataclass
class DataInput():
    ''''
    comments
    '''
    command: str = field(init=False)
    city: str = field(init=False)
    country: str = field(init=False)
    units: str = field(init=False)
    days: str = field(init=False)

    @staticmethod
    def type_days(str_days: str) -> int:
        '''
        validate days argument
        '''
        try:
            days = int(str_days)
        except ValueError as value_error:
            raise argparse.ArgumentTypeError(
                "argument days must be and integer") from value_error
        if days < 1 or days > 5:
            raise argparse.ArgumentTypeError(
                "argument days must be and integer number between 1 and 5")
        return days

    @staticmethod
    def type_location(location: str):
        '''
        validate location argument
        '''
        try:
            city, country_code = location.split(",")
        except ValueError as value_error:
            raise argparse.ArgumentTypeError(
                "argument location must be in {city},{country code} format.") from value_error
        if not city.isalpha():
            raise argparse.ArgumentTypeError(f"city:{city} not valid")
        if not country_code.isalpha():
            raise argparse.ArgumentTypeError(
                f"country:{country_code} not valid")
        if len(country_code) < 2 or len(country_code) > 3:
            raise argparse.ArgumentTypeError(
                f"country:{country_code} not valid")
        return (city, country_code)

    def get_arguments(self):
        '''
        Get Arguments from console
        '''

        parser = argparse.ArgumentParser(
            description="Get the current or forecast weather for the given location")

        parser.add_argument("command", type=str, choices=(
            Const.CURRENT, Const.FORECAST), help="Current for today or forecast for the next days")
        parser.add_argument("location", type=DataInput.type_location,
                            help="Location in {city},{country_code} format.")
        parser.add_argument("--days", type=DataInput.type_days, default=1,
                            help="Number of days to retrieve forecast data for, 1 by default,5 max")
        parser.add_argument("--units", choices=(Const.METRIC, Const.IMPERIAL), default=Const.METRIC,
                            help="Units of measurement (metric or imperial), metric by default.")

        args = parser.parse_args()
        self.command = args.command
        self.city = args.location[0]
        self.country = args.location[1]
        self.units = args.units
        self.days = args.days
