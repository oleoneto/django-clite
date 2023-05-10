from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from {{ project }}.{{ app }}.{{ name }} import {{ classname }}


class {{ classname }}TestCase(APITestCase):

    # The client used to connect to the API
    client = APIClient()

    fixtures = []

    def setUp(self):
        # API endpoint
        self.namespace = '/v1/{{ namespace }}'
        self.user = get_user_model().objects.get(id=1)
        self.record = {{ classname }}.objects.create({})

    def test_not_allowed_to_create_record_when_unauthenticated(self):
        res = self.client.post(self.namespace)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
