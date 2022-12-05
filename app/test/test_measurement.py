import unittest

import json
from dateutil import parser
from app.test.base import BaseTestCase


def store_measurement(self):
    timestamp_utc = parser.parse('2022-12-05T11:54:52.301Z')
    return self.client.post(
        '/measurement/',
        data=json.dumps(dict(
            sensor_id=1,
            measurement_type_id=1,
            value=0.123,
            timestamp_utc='2022-12-05T11:54:52.301Z'
        )),
        content_type='application/json'
    )


class TestMeasurement(BaseTestCase):
    def test_get_all_measurements_initial(self):
        """ Test get all measurements initial """
        with self.client:
            response = self.client.get('/measurement/')
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 0)
            self.assertEqual(response.status_code, 200)

    def test_registration(self):
        """ Test for store measurement """
        with self.client:
            response = store_measurement(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully created.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_get_all_measurements_after_store(self):
        """ Test get all measurements after store """
        store_measurement(self)
        with self.client:
            response = self.client.get('/measurement/')
            data = json.loads(response.data.decode())
            # self.assertEqual(data, 'xxx')
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'][0]['sensor_id'], 1)
            self.assertEqual(data['data'][0]['measurement_type_id'], 1)
            self.assertEqual(response.status_code, 200)

    def test_get_all_measurements_with_additional_params_not_empty(self):
        """ Test get all measurements after store """
        store_measurement(self)
        with self.client:
            response = self.client.get('/measurement/?sensor_id=1&measurement_type_id=1&limit=2&order_type=asc')
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'][0]['sensor_id'], 1)
            self.assertEqual(data['data'][0]['measurement_type_id'], 1)
            self.assertEqual(response.status_code, 200)

    def test_get_all_measurements_with_additional_params_empty(self):
        """ Test get all measurements after store """
        store_measurement(self)
        with self.client:
            response = self.client.get('/measurement/?sensor_id=2')
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 0)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
