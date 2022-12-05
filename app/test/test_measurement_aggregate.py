import unittest

import json
from dateutil import parser
from datetime import timedelta
from app.test.base import BaseTestCase


def store_one_measurement(self):
    self.client.post(
        '/measurement/',
        data=json.dumps(dict(
            sensor_id=1,
            measurement_type_id=2,
            value=1,
            timestamp_utc='2022-12-01T01:01:01.301Z'
        )),
        content_type='application/json'
    )


def store_hundreds_measurement(self):
    timestamp_input = '2022-12-01T01:01:01.301Z'
    value_input = 1
    for i in range(100):
        self.client.post(
            '/measurement/',
            data=json.dumps(dict(
                sensor_id=1,
                measurement_type_id=1,
                value=value_input,
                timestamp_utc=timestamp_input
            )),
            content_type='application/json'
        )
        new_timestamp_input_dt = parser.parse(
            timestamp_input) + timedelta(minutes=2)
        timestamp_input = new_timestamp_input_dt.isoformat()

        value_input += 0.5

class TestMeasurement(BaseTestCase):
    def test_get_all_measurements_initial(self):
        """ Test get all measurements initial """
        with self.client:
            response = self.client.get(
                '/measurement/?sensor_id=1&measurement_type_id=1&limit=1000')
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 0)
            self.assertEqual(response.status_code, 200)

    def test_get_all_measurements_final(self):
        """ Test get all measurements initial """
        store_one_measurement(self)
        store_hundreds_measurement(self)
        with self.client:
            response_all = self.client.get(
                '/measurement/?limit=1000')
            data_all = json.loads(response_all.data.decode())
            self.assertEqual(len(data_all['data']), 101)

            response = self.client.get(
                '/measurement/?sensor_id=1&measurement_type_id=1&limit=1000')
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 100)
            self.assertEqual(data['data'][0]['timestamp_utc'],
                             '2022-12-01T01:01:01.301000')
            self.assertEqual(data['data'][0]['sensor_id'], 1)
            self.assertEqual(data['data'][0]['measurement_type_id'], 1)
            self.assertEqual(data['data'][0]['value'], 1)
            self.assertEqual(data['data'][99]['timestamp_utc'],
                             '2022-12-01T04:19:01.301000')
            self.assertEqual(data['data'][99]['value'], 50.5)
            self.assertEqual(response.status_code, 200)

    def test_get_hourly_measurement_aggregates_empty(self):
        """ Test get hourly empty measurements aggregates """
        store_one_measurement(self)
        store_hundreds_measurement(self)
        with self.client:
            start_time = '2022-12-01T01:01:01.301000'
            end_time = '2022-12-01T04:19:01.301000'
            time_split = '1h'
            response = self.client.get(
                f'/measurement/aggregate?sensor_id=100&measurement_type_id=1&time_split={time_split}&start_time={start_time}&end_time={end_time}')
            data = json.loads(response.data.decode())
            self.assertEqual(data['start_time'], start_time)
            self.assertEqual(data['end_time'], end_time)
            self.assertEqual(data['time_split'], time_split)
            self.assertEqual(data['sensor_id'], 100)
            self.assertEqual(data['measurement_type_id'], 1)
            self.assertEqual(len(data['list_time']), 0)
            self.assertEqual(len(data['list_min_value']), 0)

    def test_get_per_15min_measurement_aggregates_empty(self):
        """ Test get hourly empty measurements aggregates """
        store_one_measurement(self)
        store_hundreds_measurement(self)
        with self.client:
            start_time = '2022-12-01T01:01:01.301000'
            end_time = '2022-12-01T04:19:01.301000'
            time_split = '15min'
            response = self.client.get(
                f'/measurement/aggregate?sensor_id=100&measurement_type_id=1&time_split={time_split}&start_time={start_time}&end_time={end_time}')
            data = json.loads(response.data.decode())
            self.assertEqual(data['start_time'], start_time)
            self.assertEqual(data['end_time'], end_time)
            self.assertEqual(data['time_split'], time_split)
            self.assertEqual(data['sensor_id'], 100)
            self.assertEqual(data['measurement_type_id'], 1)
            self.assertEqual(len(data['list_time']), 0)
            self.assertEqual(len(data['list_min_value']), 0)

    def test_get_per_15min_measurement_aggregates(self):
        """ Test get all measurements aggregates """
        store_one_measurement(self)
        store_hundreds_measurement(self)
        with self.client:
            start_time = '2022-12-01T01:01:01.301000'
            end_time = '2022-12-01T02:19:01.301000'
            time_split = '15min'
            response = self.client.get(
                f'/measurement/aggregate?sensor_id=1&measurement_type_id=1&time_split={time_split}&start_time={start_time}&end_time={end_time}')
            data = json.loads(response.data.decode())
            self.assertEqual(data['start_time'], start_time)
            self.assertEqual(data['end_time'], end_time)
            self.assertEqual(data['time_split'], time_split)
            self.assertEqual(data['sensor_id'], 1)
            self.assertEqual(data['measurement_type_id'], 1)
            self.assertEqual(data['list_min_value'][0], 1.0)
            self.assertEqual(data['list_mean_value'][0], 2.50)
            self.assertEqual(data['list_mean_value'][-1], 20)
            self.assertEqual(data['list_max_value'][-1], 20.5)
            self.assertEqual(data['list_time'][0], '2022-12-01T01:00:00')
            self.assertEqual(data['list_time'][-1], '2022-12-01T02:15:00')


if __name__ == '__main__':
    unittest.main()
