import unittest

import json
from app.test.base import BaseTestCase


def register_measurement_type(self):
    return self.client.post(
        '/measurement-type/',
        data=json.dumps(dict(
            title='Measurement type 1',
            info='Info measurement type 1'
        )),
        content_type='application/json'
    )


def get_all_measurement_types(self):
    return self.client.get('/measurement-type/')


class TestMeasurementType(BaseTestCase):
    def test_get_all_measurement_types_initial(self):
        """ Test get all measurement types initial"""
        with self.client:
            response = get_all_measurement_types(self)
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 0)
            self.assertEqual(response.status_code, 200)

    def test_registration(self):
        """ Test for measurement type registration """
        with self.client:
            response = register_measurement_type(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully created.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_measurement_type(self):
        """ Test registration new measurement type with already registered title """
        register_measurement_type(self)
        with self.client:
            response = register_measurement_type(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Measurement type already exists.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def test_get_all_measurement_types_after_register(self):
        """ Test get all measurement types after register"""
        register_measurement_type(self)
        with self.client:
            response = get_all_measurement_types(self)
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'][0]['title'], "Measurement type 1")
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
