from django.test import TestCase

from airMonitor.models.Chart import Chart


class TestChartWrapper(TestCase):
    def test_file_load(self):
        chart = Chart()
        self.assertIn("type", chart.dict())
        self.assertIn("data", chart.dict())
        self.assertIn("options", chart.dict())

    def test_empty_data(self):
        chart = Chart()
        self.assertEqual(len(chart._datasets), 0)

    def test_add_data_same_key(self):
        chart = Chart()
        for i in range(10):
            chart.add_data("key", i)
        self.assertEqual(len(chart._datasets), 1)

    def test_add_data_multiple_keys(self):
        chart = Chart()
        for key in ["key1", "key2", "key3", "key4"]:
            for i in range(10):
                chart.add_data(key, i)
        self.assertEqual(len(chart._datasets), 4)
    