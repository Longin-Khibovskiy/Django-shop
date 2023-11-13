from rest_framework.test import APITestCase
from django.urls import reverse
from shoes.models import Shoes
from shoes.serializers import ShoesSerializer
from rest_framework import status

class ShoesApiTestCase(APITestCase):
    def test_get_list(self):
        shoes_1 = Shoes.objects.create(name='Lebron 19', price=15)
        shoes_2 = Shoes.objects.create(name='Air Force 1', price=25)

        response = self.client.get(reverse('shoes_api_list'))

        serial_data = ShoesSerializer([shoes_1, shoes_2], many=True).data
        serial_data = {'shoes_list': serial_data}

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serial_data, response.data)
