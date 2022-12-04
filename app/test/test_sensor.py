import unittest

import json
from app.test.base import BaseTestCase


def register_sensor(self):
    return self.client.post(
        '/sensor/',
        data=json.dumps(dict(
            title='Sensor 1',
            info='Info sensor 1'
        )),
        content_type='application/json'
    )


def get_all_sensors(self):
    return self.client.get('/sensor/')


class TestSensor(BaseTestCase):
    def test_get_all_sensors_initial(self):
        """ Test get all sensors initial"""
        with self.client:
            response = get_all_sensors(self)
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 0)
            self.assertEqual(response.status_code, 200)

    def test_registration(self):
        """ Test for sensor registration """
        with self.client:
            response = register_sensor(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully created.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_sensor(self):
        """ Test registration new sensor with already registered title """
        register_sensor(self)
        with self.client:
            response = register_sensor(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Sensor already exists.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def test_get_all_sensors_after_register(self):
        """ Test get all sensors after register"""
        register_sensor(self)
        with self.client:
            response = get_all_sensors(self)
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'][0]['title'], "Sensor 1")
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
