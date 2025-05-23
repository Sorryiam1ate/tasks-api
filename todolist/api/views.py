from datetime import datetime

import requests
from api.models import AstanaHubParticipant
from bs4 import BeautifulSoup
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer


class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['completed']
    search_fields = ['title']
    pagination_class = TaskPagination


class ParseAstanaHubView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Парсинг данных с сайта AstanaHub",
        request_body=None,
        responses={201: openapi.Response(
            description="Данные успешно получены")}
    )
    def post(self, request):
        url = 'https://astanahub.com/ru/service/techpark/'
        response = requests.get(url)
        if response.status_code != 200:
            return Response(
                {'error': 'Failed to fetch data from Astana Hub'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        soup = BeautifulSoup(response.text, 'html.parser')

        table_div = soup.find('div', class_='table-overflow')

        if table_div:
            table = table_div.find('table', class_='table')
            if table:
                rows = table.find_all('tr')[1:11]
                for row in rows:
                    td_rows = row.find_all('td')
                    certificate_number = td_rows[0].get_text(strip=True)
                    issue_date_str = td_rows[1].get_text(strip=True)
                    expiry_date_str = td_rows[2].get_text(strip=True)
                    bin_number = td_rows[3].get_text(strip=True)
                    status_text = td_rows[4].get_text(strip=True)
                    company_name = td_rows[5].get_text(strip=True)
                    issue_date = datetime.strptime(
                        issue_date_str, '%Y-%m-%d').date()
                    expiry_date = datetime.strptime(
                        expiry_date_str, '%Y-%m-%d').date()

                    stat = True if status_text.lower() == 'активно' else False

                    participant, created = AstanaHubParticipant.objects.get_or_create(
                        certificate_number=certificate_number,
                        defaults={
                            'issue_date': issue_date,
                            'expiration_date': expiry_date,
                            'bin': bin_number,
                            'status': stat,
                            'company_name': company_name
                        }
                    )
        return Response(
            {'result': 'Данные получены'},
            status=status.HTTP_201_CREATED
        )
