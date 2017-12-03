import unittest


class TestDict(unittest.TestCase):
    def test_dict(self):
        dict_test = {'key': 'value'}
        self.assertDictEqual(dict_test, {'key': 'value'})


if __name__ == '__main__':
    unittest.main()
