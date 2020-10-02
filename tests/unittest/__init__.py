import unittest
import os
from pickle_rick import BasePickleRick, ExtendedPickleRick

class TestPickles(unittest.TestCase):

    def test_base_config(self):
        # Test normal dict
        test_dict = {'A' : 1, 'l' : [1, { 'deep' : 'hole'}], 'B' : { 'k' : 'v'}}
        test_conf = BasePickleRick(test_dict)

        self.assertEquals(test_conf.A, 1)
        self.assertListEqual(test_conf.l, [1,{ 'deep' : 'hole'}])
        self.assertEquals(test_conf.B.k, 'v')

        # Test deep dict
        test_conf = BasePickleRick(test_dict, deep=True)

        self.assertEquals(test_conf.l[-1].deep, 'hole')

        # Test YAML and JSON doc loading with file path

        test_conf_yaml = BasePickleRick('./tests/placebos/test_config.yaml', deep=True)
        test_conf_json = BasePickleRick('./tests/placebos/test_config.json', deep=True)

        self.assertGreater(len(test_conf_yaml), 0)
        self.assertGreater(len(test_conf_json), 0)
        self.assertTrue(test_conf_yaml == test_conf_json)

        # Test YAML and JSON doc loading with file stream

        with open('./tests/placebos/test_config.yaml', 'r') as fs_y, open('./tests/placebos/test_config.json', 'r') as fs_j:
            test_conf_yaml = BasePickleRick(fs_y, deep=True)
            test_conf_json = BasePickleRick(fs_j, deep=True)

            self.assertGreater(len(test_conf_yaml), 0)
            self.assertGreater(len(test_conf_json), 0)
            self.assertTrue(test_conf_yaml == test_conf_json)

        # Test string loading
        yaml_string = """
                ONE: "value"
                """
        json_string = """
                { "ONE" : "value"}
                """
        test_conf_yaml = BasePickleRick(yaml_string, deep=True)
        test_conf_json = BasePickleRick(json_string, deep=True)

        self.assertTrue(test_conf_yaml == test_conf_json)
        self.assertEquals(test_conf_yaml.ONE, "value")
        self.assertEquals(test_conf_json.ONE, "value")

    def test_extended_config(self):
        # Test normal dict
        test_dict = {'A' : 1, 'l' : [1, { 'deep' : 'hole'}], 'B' : { 'k' : 'v'}}
        test_conf = ExtendedPickleRick(test_dict)

        self.assertEquals(test_conf.A, 1)
        self.assertListEqual(test_conf.l, [1,{ 'deep' : 'hole'}])
        self.assertEquals(test_conf.B.k, 'v')

        # Test deep dict
        test_conf = ExtendedPickleRick(test_dict, deep=True)

        self.assertEquals(test_conf.l[-1].deep, 'hole')

        # Test extended operations (OS ENV, functions)
        test_dict = {'user' : {
                        'type'  : 'env',
                        'load': 'USERNAME'
                    },
                     'func' : {
                        'type'  : 'lambda',
                        'load': 'lambda x: x+1'
                     }
        }

        test_conf = ExtendedPickleRick(test_dict, load_lambda=True)

        expected_username = os.getenv('USERNAME')

        self.assertEquals(test_conf.user, expected_username)
        self.assertEquals(test_conf.func(41), 42)

    def test_config_get_search(self):
        test_conf_yaml = BasePickleRick('./tests/placebos/test_config.yaml', deep=True)

        value = test_conf_yaml.get('one')

        self.assertEquals(value, 'value')

        value = test_conf_yaml.get('ONE')

        self.assertEquals(value, 'value')

        value = test_conf_yaml.get('username')

        self.assertIsInstance(value, BasePickleRick)
        self.assertEquals(value.type, 'env')

    def test_config_to_dict(self):
        test_dict = {'user': {
            'type': 'env',
            'load': 'USERNAME'
            },
            'func': {
                'type': 'lambda',
                'load': 'lambda x: x+1'
            }
        }

        test_conf = BasePickleRick(test_dict)

        self.assertDictEqual(test_conf.dict(), test_dict)

    def test_config_keys(self):
        test_dict = {'user': {
            'type': 'env',
            'load': 'USERNAME'
            },
            'func': {
                'type': 'lambda',
                'load': 'lambda x: x+1'
            }
        }

        test_conf = ExtendedPickleRick(test_dict)

        for k in test_conf.keys():
            self.assertIn(k, ['user', 'func'])

    def test_config_iterator(self):
        test_dict = {'user': {
            'hello' : 'world'
            },
            'func': {
                'hello' : 'world'
            }
        }

        test_conf = ExtendedPickleRick(test_dict)

        for k in test_conf:
            self.assertEquals(k.hello, 'world')

    def test_config_has_key(self):
        test_dict = {'user': {
            'hello' : 'world'
            },
            'func': {
                'hello' : 'world'
            }
        }

        test_conf = ExtendedPickleRick(test_dict)

        self.assertTrue(test_conf.has('user'))
        self.assertFalse(test_conf.has('hello'))
        self.assertTrue(test_conf.has('hello', deep=True))
        self.assertFalse(test_conf.has('BYE', deep=True))
        self.assertFalse(test_conf.has('BYE', deep=False))
