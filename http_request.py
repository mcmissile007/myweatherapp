'''
comments
'''

import requests


class HttpRequest():
    '''
    comments
    '''

    def ___init__(self):
        pass

    @staticmethod
    def simple_http_request(url: str, query: dict) -> str:
        '''
        simple GET http_request without auth.
        @param url:
        @param query: dict with the query string params
        @retunn: text response from server or "" if error
        '''
        try:
            response = requests.get(url, params=query, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.exceptions.ConnectionError as errc:
            print(f"connection error {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"timeout error: {errt}")
        except requests.exceptions.HTTPError as errh:
            print(f"http error: {errh}")
        except requests.RequestException as err:
            print(f"generic requests error:{err}")
        return ""
