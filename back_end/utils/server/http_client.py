import json
import requests
import typing
from urllib.parse import urlencode


# HTTPClient class: used to consume external rest services
class HttpClient(object):

    def __init__(self, token: str, headers: dict = {}):
        # Constructor for any API client
        self.__headers = self.mergeDict({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'bearer %s' % token
        }, headers)

    def cleanDict(self, x: dict = {}) -> dict:
        result = {}
        for key in x:
            if x[key] is not None:
                # Check If List
                if isinstance(x[key], (list,)):
                    result[key] = ','.join(x[key])
                # Check If Boolean
                elif isinstance(x[key], (bool)):
                    if x[key] is True:
                        result[key] = 'true'
                    else:
                        result[key] = 'false'
                # Everything Else (Strings/Numbers)
                else:
                    result[key] = x[key]
        return result

    def mergeDict(self, x: dict, y: dict) -> dict:
        z = self.cleanDict(x)
        z.update(self.cleanDict(y))
        return z

    def buildUrlWithParams(self, url: str, params={}) -> str:
        encoded = urlencode(self.cleanDict(params))
        return url if (len(encoded) == 0) else (url + '?' + encoded)

    def __validator(self, result: requests.Response) -> typing.Union[str, dict]:
        try:
            body = json.loads(result.text)
        except Exception:
            body = {}

        if type(body) is dict and body.get('code', None) is not None:
            raise Exception(body.get('description'))
        elif result.status_code >= 400:
            raise Exception(' '.join([str(result.status_code), result.reason]))
        elif len(result.text) == 0:
            return 'OK'
        else:
            return body

    def request(self, method: str, url: str, data: any = {}, params: dict = {}, headers={}) -> typing.Union[str, dict]:
        requestUrl = self.buildUrlWithParams(url, params)
        requestHeaders = self.mergeDict(self.__headers, headers)
        requestData = ''
        if type(data) is dict:
            requestData = json.dumps(data) if len(data.keys()) > 0 else ''
        if type(data) is list:
            requestData = json.dumps(data) if len(data) > 0 else ''
        result = requests.request(
            method, requestUrl, data=requestData, headers=requestHeaders)
        return self.__validator(result)
