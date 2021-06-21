from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from cars.models import Make


class MakeTestCase(TestCase):
    def test_get_existing(self):
        Make.objects.create(name='Some manifacturer')
        expected_status_code = 200
        expected_make_count = 0

        response = self.client.get(reverse('makes-list'))

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_make_count, len(response.json()['results']))

    def test_create_new_make(self):
        expected_status_code = 201
        expected_make_count = 1

        response = self.client.post(reverse('makes-list'), data={
            'name': 'Geely',
        }, content_type='application/json')

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_make_count, Make.objects.count())

    def test_update_make(self):
        expected_status_code = 200
        expected_make_name = 'Geely'
        expected_make_count = 1

        # Existing make needed
        make = Make.objects.create(name='Some manufacturer')

        response = self.client.put(reverse('make-details', args=[make.pk]), data={
            'name': expected_make_name,
        }, content_type='application/json')

        # Refresh object from db to get updates
        make.refresh_from_db()

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_make_count, Make.objects.count())
        self.assertEqual(expected_make_name, make.name)

    def test_delete_make(self):
        expected_status_code = 204
        expected_make_count = 0

        # Existing make needed
        make = Make.objects.create(name='Some manufacturer')

        response = self.client.delete(reverse('make-details', args=[make.pk]))

        make.refresh_from_db()

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_make_count, Make.objects.not_deleted().count())
