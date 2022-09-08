import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Company
from api.serializers import CompanySerializer
from api.serializers import MyTokenObtainPairSerializer, RegisterSerializer


@permission_classes([IsAuthenticated])
class CompanyView(APIView):
    """
    Company rest view class.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id: int = 0) -> JsonResponse:
        """
        returns the companies list or a certain company by its id

        :param id: the id of the company to query
        :param request: a simple Http request
        :return: an API response with the selected company
        """
        if id > 0:
            try:
                company = Company.objects.get(pk=id)
                serializer = CompanySerializer(company, context={'request': request}, many=False)
                datos = {
                    'message': 'Success.',
                    'company': serializer.data
                }
                return JsonResponse(datos)
            except Company.DoesNotExist:
                datos = {
                    'message': 'Company not found.'
                }
                return JsonResponse(datos)

        else:
            data = Company.objects.all()
            serializer = CompanySerializer(data, context={'request': request}, many=True)
            datos = {
                'message': 'Success.',
                'companies': serializer.data
            }
            return JsonResponse(datos)

    def post(self, request) -> JsonResponse:
        """
         Add a new company

         :param request: a simple Http request
         :return: a response from the API
         """
        permission_classes = (IsAuthenticated,)
        jd = json.loads(request.body)
        if len(Company.objects.all()) > 0:
            num_results = Company.objects.filter(name=jd['name']).count()
            if num_results < 1:
                serializer = CompanySerializer(data=jd)
                if serializer.is_valid():
                    serializer.save()
                    datos = {
                        'message': 'Success.'
                    }
                    return JsonResponse(datos)
            else:
                datos = {
                    'message': 'Company already exists.'
                }
                return JsonResponse(datos)
        else:
            serializer = CompanySerializer(data=jd)
            if serializer.is_valid():
                serializer.save()
                datos = {
                    'message': 'Success.'
                }
                return JsonResponse(datos)

    def put(self, request, id: int) -> JsonResponse:
        """
         Update an existing company in the DB
         :param id: the id of the object to update
         :param request: a simple Http request
         :return: a response from the API
         """
        permission_classes = (IsAuthenticated,)
        student = Company.objects.get(pk=id)
        jd = json.loads(request.body)
        serializer = CompanySerializer(student, data=jd, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            datos = {
                'message': 'Success.'
            }
            return JsonResponse(datos)
        else:
            datos = {
                'message': 'Company not found.'
            }
            return JsonResponse(datos)

    def delete(self, request, id: int) -> Response | JsonResponse:
        """
         Remove a company from the DB

         :param id: the id of the object to delete
         :param request: a simple Http request
         :return: a response from the API depending on the execution Success or not found
         """
        try:
            student = Company.objects.get(pk=id)
            student.delete()
            datos = {
                'message': 'Success.'
            }
            return JsonResponse(datos)
        except Company.DoesNotExist:
            datos = {"message": "Company not found"}
            return JsonResponse(datos)


class MyTokenObtainPairView(TokenObtainPairView):
    """Token pair vuew"""
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """Register view class"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request) -> Response:
    """Returns a response for a given route"""
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/login'
        'api/companies'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)
