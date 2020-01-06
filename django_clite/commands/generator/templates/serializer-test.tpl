from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from ..{{ model.lower() }} import {{ classname }}
from ..{{ model.lower() }} import {{ classname }}Serializer


class {{ classname }}TestCase(APITestCase):

    # The client used to connect to the API
    client = APIClient()

    # Resource endpoint namespace
    namespace = '/v1/{{ namespace }}'

    def setUp(self):
        """
        Prepare database and client.
        """

        user = get_user_model().objects.first()

        # API endpoint
        self.client.force_authenticate(user=user)

    def test_create_{{ model.lower() }}(self):
        """
        url = self.namespace
        res = self.client.post(url, data={})
        self.assertEqual(res.status_code, 201)
        """
        pass

    def test_retrieve_{{ model.lower() }}(self):
        """
        url = self.namespace + '/1'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        """
        pass

    def test_list_{{ model.lower() }}(self):
        """
        url = self.namespace
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        """
        pass

    def test_update_{{ model.lower() }}(self):
        """
        url = self.namespace + '/1'
        res = self.client.update(url, data={})
        self.assertEqual(res.status_code, 202)
        """
        pass

    def test_delete_{{ model.lower() }}(self):
        """
        url = self.namespace + '/1'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)
        """
        pass
