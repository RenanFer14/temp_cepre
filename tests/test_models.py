from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from app.models import *


class ColegioTestAPICase(APITestCase):
    def setUp(self) -> None:
        self.urlcolegios = reverse('colegio_list')

    def test_colegio(self):
        ubigeo.objects.create(
            codigo_ubigeo='080101', nombre = 'Cusco', tipo_ubigeo = 'T'
        )
        ubigeo.objects.create(
            codigo_ubigeo='080102', nombre = 'Wanchaq', tipo_ubigeo = 'T'
        )
        cusco = ubigeo.objects.get(codigo_ubigeo='080101')
        wanchaq = ubigeo.objects.get(codigo_ubigeo='080102')

        self.assertEquals(colegio.objects.count(), 0)
        colegio.objects.create(
            ubigeo_id= cusco.codigo_ubigeo, nombre_colegio='Colegio 01', tipo_colegio='PU'
        )
        self.assertEquals(colegio.objects.count(), 1)

        data = {
            'ubigeo_id': cusco.codigo_ubigeo,
            'nombre_colegio': 'Colegio 02',
            'tipo_colegio': 'PU'
        }
        response = self.client.post(self.urlcolegios, data, format='json')
        self.assertEquals(colegio.objects.count(), 2)

        data = response.data
        print(data)
        data['nombre_colegio'] = 'Colegio 02 modificado'
        data['ubigeo_id'] = wanchaq.codigo_ubigeo
        response = self.client.put(self.urlcolegios+'/'+str(data['id']), data, format='json')
        self.assertEquals(colegio.objects.count(), 2)
        response = self.client.get(self.urlcolegios+'/'+str(data['id']), format='json')
        self.assertEquals(colegio.objects.count(), 2)
        data = response.data
        print(data)
        response = self.client.delete(self.urlcolegios+'/'+str(data['id']), format='json')
        self.assertEquals(colegio.objects.count(), 1)
