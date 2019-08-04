from django.contrib.auth import get_user_model
from django.test import TestCase
from django_dynamic_fixture import G
from rest_framework.test import APIClient


class TestRegistration(TestCase):

    def setUp(self):
        self.user_class = get_user_model()
        self.client = APIClient()
        self.create_test_user(name='test', email='e@ma.il', password="fdhfeyteb", is_active=True)

    def create_test_user(self, **kwargs):
        password = kwargs.pop('password', None)
        user = G(self.user_class, **kwargs)
        if password is not None:
            user.set_password(password)
            user.save()
            user.password_in_plaintext = password
        return user

    def test_registration(self):
        data = {
            "name": "testuser",
            "email": "test@test.test",
            "phone": "12345",
            "language": "English",
            "currency": "USD",
            "password": "4hchtvhr",
            "password_confirm": "4hchtvhr"
        }

        response = self.client.post('/api/providers/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_registration_only_email(self):
        data = {
            "email": "test2@test.test",
            "phone": "",
            "language": "",
            "currency": "",
            "password": "4hchtvhr",
            "password_confirm": "4hchtvhr"
        }

        response = self.client.post('/api/providers/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_add_polygon(self):
        data = {
            "name": "string",
            "price": 0,
            "provider": 1,
            "polygon": {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0.0, 0.0], [0.0, 100.0], [100.0, 100.0], [100.0, 0.0], [0.0, 0.0]]]
                    }
                }]
            }
        }

        # 50.0, 50.0 should not return a servicearea
        response = self.client.get('/api/serviceareas/by-lat-lon/50/50/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/api/serviceareas/', data, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/serviceareas/', data, format='json')
        self.assertEqual(response.status_code, 200)

        # 50.0, 50.0 should now return a servicearea
        response = self.client.get('/api/serviceareas/by-lat-lon/50/50/')
        self.assertEqual(response.status_code, 200)
