from  cpmAPI.models import Trabajador
from oauth.serializers.login_serializer import LoginSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView
from utils.server.rest_utils import ApiRestUtilities


#Login endpoint
class Login(CreateAPIView):
    queryset = Trabajador.objects.all()
    serializer_class = LoginSerializer


    #POST Request
    def post(self, request, *args, **kwargs):
        login_serializer = LoginSerializer(data=request.data)
        if(login_serializer.is_valid(raise_exception=True)):
            user, token = login_serializer.save()
            data = {
                'profile': user,
                'token': token
            }

            #Returns token login
            return ApiRestUtilities.get_rest_successfull_response(
                "Succesful login",
                data,
                status.HTTP_200_OK
            )