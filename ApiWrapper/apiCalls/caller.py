import requests
from nap.url import Url
from datetime import date
from datetime import timedelta


'''
    classe que gerencia todas as chamadas diretas a api do currency layer
'''


class ApiCaller(object):

    def __init__(self, token, *currencies):

        self._APIS = {
                    "history": "historical",
                    "current": "live",
                    "currencies": "list"
                }
        self._base_data = {
                    "access_key": token,
                    "format": 0,
                    "currencies": ""
                }
        self.url = "http://apilayer.net/api/"

        self._TOKEN = token
        self.insert(*currencies)
        self._api = Url(self.url)

    def insert(self, *currencies):
        for currencie in currencies:
            if len(self._base_data["currencies"]) == 0:
                self._base_data["currencies"] = currencie.initials()
                continue
            self._base_data["currencies"] = ','.join(
                                                (self._base_data["currencies"],
                                                    currencie.initials())
                                                )

    def live(self):
        return self._api.get('live', params=self._base_data).json()

    def history(self, daterange):
        json_response = {"response": []}
        today = date.today()
        day = timedelta(days=1)
        myparams = self._base_data.copy()

        for i in range(daterange, 0, -1):
            myparams["date"] = (today - i*day).isoformat()
            response = self._api.get('historical', params=myparams)
            if response.status_code != 200:
                raise('Response was not OK, it was: %s' % e.response.status_code)
            responseObj = response.json()
            if not responseObj["success"]:
                print("Error on get api data:")
                print(responseObj)
            json_response["response"].append(response.json())
        return json_response
