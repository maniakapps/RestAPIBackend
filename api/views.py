import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def company_view(request, id: int = 0):
    """
    Returns the companies list or a certain company by its id.

    :param id: The id of the company to query.
    :param request: A simple HTTP request.
    :return: An API response with the selected company.
    """
    if id > 0:
        company = get_object_or_404(Company, pk=id)
        if not request.user.has_perm('view_company', company):
            return Response({'message': 'Not authorized to view company.'}, status=403)
        serializer = CompanySerializer(company, context={'request': request}, many=False)
        return Response({'message': 'Success.', 'company': serializer.data})
    else:
        if not request.user.has_perm('view_company', Company):
            return Response({'message': 'Not authorized to view companies.'}, status=403)
        data = list(Company.objects.all())
        serializer = CompanySerializer(data, context={'request': request}, many=True)
        return Response({'message': 'Success.', 'companies': serializer.data})

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

class CompanyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request) -> Response:
        """
        Add a new company
        :param request: a simple HTTP request
        :return: a response from the API
        """
        jd = request.data
        num_results = Company.objects.filter(name=jd['name']).count()
        if num_results < 1:
            serializer = CompanySerializer(data=jd)
            if serializer.is_valid():
                serializer.save()
                datos = {'message': 'Success.'}
                return Response(datos)
        else:
            datos = {'message': 'Company already exists.'}
            return Response(datos, status=400)

    def put(self, request, id: int) -> Response:
        """
         Update an existing company in the DB
         :param id: the id of the object to update
         :param request: a simple HTTP request
         :return: a response from the API
         """
        student = get_object_or_404(Company, pk=id)
        jd = request.data
        serializer = CompanySerializer(student, data=jd, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            datos = {'message': 'Success.'}
            return Response(datos)
        else:
            datos = {'message': 'Company not found.'}
            return Response(datos, status=404)

    def delete(self, request, id: int) -> Response:
        """
         Remove a company from the DB
         :param id: the id of the object to delete
         :param request: a simple HTTP request
         :return: a response from the API depending on the execution Success or not found
         """
        try:
            student = Company.objects.get(pk=id)
            student.delete()
            datos = {'message': 'Success.'}
            return Response(datos)
        except Company.DoesNotExist:
            datos = {'message': 'Company not found'}
            return Response(datos, status=404)



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


class TestEndpointView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = f"Congratulations {request.user}, your API just responded to GET request."
        return Response({'response': data}, status=status.HTTP_200_OK)

    def post(self, request):
        text = request.data.get('text')
        data = f'Congratulations, your API just responded to POST request with text: {text}.'
        return Response({'response': data}, status=status.HTTP_200_OK)
