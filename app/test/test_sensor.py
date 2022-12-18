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


def get_a_sensor(self, sensor_id):
    return self.client.get(f'/sensor/{sensor_id}')


def delete_a_sensor(self, sensor_id):
    return self.client.delete(f'/sensor/{sensor_id}')


def update_a_sensor(self, sensor_id):
    return self.client.put(
        f'/sensor/{sensor_id}',
        data=json.dumps(dict(
            title='Sensor 1 update',
            info='Info sensor 1 update'
        )),
        content_type='application/json'
    )


class TestSensor(BaseTestCase):
    def test_get_all_sensors_initial(self):
        """ Test get all sensors initial """
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
        """ Test get all sensors after register """
        register_sensor(self)
        with self.client:
            response = get_all_sensors(self)
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'][0]['title'], "Sensor 1")
            self.assertEqual(response.status_code, 200)
    
    def test_get_specific_sensor_after_register(self):
        """ Test get specific sensor after register """
        register_sensor(self)
        with self.client:
            response = get_a_sensor(self, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['title'], "Sensor 1")
            self.assertEqual(response.status_code, 200)
    
    def test_failed_get_specific_sensor_after_register(self):
        """ Test failed get specific sensor not exist """
        with self.client:
            response = get_a_sensor(self, 1000)
            self.assertEqual(response.status_code, 404)
    
    def test_delete_sensor_after_register(self):
        """ Test delete sensor after register """
        register_sensor(self)
        with self.client:
            response = delete_a_sensor(self, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully deleted.')
            self.assertEqual(response.status_code, 200)
    
    def test_failed_delete_specific_sensor_after_register(self):
        """ Test failed get specific sensor not exist """
        register_sensor(self)
        with self.client:
            response = delete_a_sensor(self, 1000)
            self.assertEqual(response.status_code, 404)
    
    def test_update_sensor_after_register(self):
        """ Test update sensor after register """
        register_sensor(self)
        with self.client:
            response_update = update_a_sensor(self, 1)
            data_update = json.loads(response_update.data.decode())
            self.assertTrue(data_update['status'] == 'success')
            self.assertTrue(data_update['message'] == 'Successfully updated.')
            self.assertEqual(response_update.status_code, 200)
            response_get = get_a_sensor(self, 1)
            data_get = json.loads(response_get.data.decode())
            self.assertEqual(data_get['title'], "Sensor 1 update")
            self.assertEqual(data_get['info'], "Info sensor 1 update")
            self.assertEqual(response_get.status_code, 200)
    
    def test_failed_update_specific_sensor_after_register(self):
        """ Test failed get specific sensor not exist """
        register_sensor(self)
        with self.client:
            response = update_a_sensor(self, 1000)
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
