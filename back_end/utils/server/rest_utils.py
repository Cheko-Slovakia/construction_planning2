from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from utils.server.http_client import HttpClient

#Class used to send a custom rest reponses in case of validation errors.
class CustomValidationError(APIException):


    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            try:
                self.detail = {field: force_text(detail)}
            except:
                self.detail = {'detail': force_text(self.default_detail)}
        else:
            self.detail = {'detail': force_text(self.default_detail)}

#Class used to manage the rest operations in the app.
class ApiRestUtilities:


    def __init__(self) -> None:
        pass

    def get_rest_successfull_response(message, data, status_code):
        return Response({
            "message": message,
            "data": data
        }, status=status_code)

    def get_rest__validation_error_response(detail, field, status_code):
        raise CustomValidationError(detail, field, status_code)

    def requested_external_service(method: str, token: str, url: str, data: any = {}, params: dict = {}, headers={}):
        httpClient = HttpClient(token, headers)
        return httpClient.request(method, url, data, params, headers)