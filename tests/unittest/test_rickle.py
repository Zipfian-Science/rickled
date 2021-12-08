import unittest
import os
from rickled import BaseRickle, Rickle

class TestPickles(unittest.TestCase):

    def test_base_config(self):
        # Test normal dict
        test_dict = {'A' : 1, 'l' : [1, { 'deep' : 'hole'}], 'B' : { 'k' : 'v'}}
        test_conf = BaseRickle(test_dict)

        self.assertEquals(test_conf.A, 1)
        self.assertListEqual(test_conf.l, [1,{ 'deep' : 'hole'}])
        self.assertEquals(test_conf.B.k, 'v')

        # Test deep dict
        test_conf = BaseRickle(test_dict, deep=True)

        self.assertEquals(test_conf.l[-1].deep, 'hole')

        # Test YAML and JSON doc loading with file path

        test_conf_yaml = BaseRickle('./tests/placebos/test_config.yaml', deep=True)
        test_conf_json = BaseRickle('./tests/placebos/test_config.json', deep=True)

        self.assertGreater(len(test_conf_yaml), 0)
        self.assertGreater(len(test_conf_json), 0)

        # Test YAML and JSON doc loading with file stream

        with open('./tests/placebos/test_config.yaml', 'r') as fs_y, open('./tests/placebos/test_config.json', 'r') as fs_j:
            test_conf_yaml = BaseRickle(fs_y, deep=True)
            test_conf_json = BaseRickle(fs_j, deep=True)

            self.assertGreater(len(test_conf_yaml), 0)
            self.assertGreater(len(test_conf_json), 0)

        # Test string loading
        yaml_string = """
                ONE: "value"
                """
        json_string = """
                { "ONE" : "value"}
                """
        test_conf_yaml = BaseRickle(yaml_string, deep=True)
        test_conf_json = BaseRickle(json_string, deep=True)

        self.assertTrue(test_conf_yaml == test_conf_json)
        self.assertEquals(test_conf_yaml.ONE, "value")
        self.assertEquals(test_conf_json.ONE, "value")

    def test_base_config_add_attr(self):
        test_conf = BaseRickle()

        test_conf.add_attr('new_var', 42)

        self.assertEquals(test_conf.new_var, 42)

        test_conf.new_var += 1

        self.assertEquals(test_conf.new_var, 43)

    def test_extended_config(self):
        # Test normal dict
        test_dict = {'A' : 1, 'l' : [1, { 'deep' : 'hole'}], 'B' : { 'k' : 'v'}}
        test_conf = Rickle(test_dict)

        self.assertEquals(test_conf.A, 1)
        self.assertListEqual(test_conf.l, [1,{ 'deep' : 'hole'}])
        self.assertEquals(test_conf.B.k, 'v')

        # Test deep dict
        test_conf = Rickle(test_dict, deep=True)

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

        test_conf = Rickle(test_dict, load_lambda=True)

        expected_username = os.getenv('USERNAME')

        self.assertEquals(test_conf.user, expected_username)
        self.assertEquals(test_conf.func(41), 42)

    def test_config_get_search(self):
        test_conf_yaml = BaseRickle('./tests/placebos/test_config.yaml', deep=True)

        value = test_conf_yaml.get('one')

        self.assertEquals(value, 'value')

        value = test_conf_yaml.get('ONE')

        self.assertEquals(value, None)

        value = test_conf_yaml.get('USERNAME')

        self.assertIsInstance(value, BaseRickle)
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

        test_conf = BaseRickle(test_dict)

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

        test_conf = Rickle(test_dict)

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

        test_conf = Rickle(test_dict)

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

        test_conf = Rickle(test_dict)

        self.assertTrue(test_conf.has('user'))
        self.assertFalse(test_conf.has('hello'))
        self.assertTrue(test_conf.has('hello', deep=True))
        self.assertFalse(test_conf.has('BYE', deep=True))
        self.assertFalse(test_conf.has('BYE', deep=False))

    def test_config_values(self):
        test_dict = {
            'user': 'BYE',
            'func': 'hello'
        }

        expected = ['BYE', 'hello']

        test_conf = BaseRickle(test_dict)

        l = test_conf.values()

        self.assertListEqual(l, expected)

    def test_config_items(self):
        test_dict = {
            'user': 'BYE',
            'func': 'hello'
        }

        test_conf = BaseRickle(test_dict)

        for k, v in test_conf.items():
            self.assertEquals(v, test_dict[k])

    def test_dump_yaml(self):
        import os

        test_dict = {'user': {
            'type': 'env',
            'load': 'USERNAME'
        },
            'func': {
                'type': 'lambda',
                'load': 'lambda x: x+1'
            }
        }

        conf = BaseRickle(test_dict)

        dumped_string = conf.to_yaml_string()

        self.assertTrue('env' in dumped_string)
        self.assertTrue('USERNAME' in dumped_string)
        self.assertTrue('lambda x: x+1' in dumped_string)

        filename = './unit_test_file_dump.yaml'

        conf.to_yaml_file(filename)

        self.assertTrue(os.path.isfile(filename))

        os.remove(filename)

    def test_dump_json(self):
        test_dict = {'user': {
            'type': 'env',
            'load': 'USERNAME'
        },
            'func': {
                'type': 'lambda',
                'load': 'lambda x: x+1'
            }
        }

        conf = BaseRickle(test_dict)

        dumped_string = conf.to_json_string()
        expected = '{"user": {"type": "env", "load": "USERNAME"}, "func": {"type": "lambda", "load": "lambda x: x+1"}}'

        self.assertEquals(dumped_string, expected)

        filename = './unit_test_file_dump.json'

        conf.to_json_file(filename)

        self.assertTrue(os.path.isfile(filename))

        os.remove(filename)

    def test_extended_config_add_function(self):
        import math
        test_conf = Rickle()

        load = """
def tester(x, c):
    y = x * 2 + c
    return math.cos(y)
        """

        args = {
            'x' : 0.42,
            'c' : 1.7
        }

        imports = ['math']

        test_conf.add_function('tester',load, args, imports)

        y = test_conf.tester(x=0.66, c=1.6)

        y_true = math.cos(0.66 * 2 + 1.6)

        self.assertEquals(y, y_true)

    def test_extended_config_add_lambda(self):
            from datetime import datetime as dd
            test_conf = Rickle()

            load = "lambda: dd.utcnow().strftime('%Y-%m-%d')"

            imports = ['from datetime import datetime as dd']

            test_conf.add_lambda('date_str', load, imports)

            y = test_conf.date_str()

            y_true = dd.utcnow().strftime('%Y-%m-%d')

            self.assertEquals(y, y_true)

    def test_pickle_rick_dict_decon(self):
        test_conf_yaml = Rickle('./tests/placebos/test_config.yaml', deep=True, load_lambda=True)

        d = test_conf_yaml.dict()

        s = test_conf_yaml.to_yaml_string()

    def test_pickle_rick_load_param(self):
        test_conf_yaml = Rickle('./tests/placebos/test_config.yaml', deep=True, arg_name='hallo_wereld', load_lambda=True)

        d = test_conf_yaml.dict()

        s = test_conf_yaml.to_yaml_string()

        s = test_conf_yaml.to_yaml_string(serialised=False)

        test_conf_yaml = Rickle('./tests/placebos/test_config.yaml', deep=True,
                                load_lambda=True)

        d = test_conf_yaml.dict()

        s = test_conf_yaml.to_yaml_string()

    def test_multi_file_load(self):
        files = ['./tests/placebos/test_config.yaml', './tests/placebos/test_second.yaml']
        test_conf_yaml = Rickle(files, deep=True, load_lambda=True)

        self.assertTrue(True)

    def test_class_definition(self):

        files = ['./tests/placebos/test_config.yaml', './tests/placebos/test_second.yaml']
        test_conf_yaml = Rickle(files, deep=True, load_lambda=True)

        obj = test_conf_yaml.TesterClass()
        obj.datenow()
        obj.math_e(99, 99)
        obj.math_e()

        self.assertTrue(True)

    def test_load_dump_load(self):
        files = ['./tests/placebos/test_config.yaml', './tests/placebos/test_second.yaml']
        test_conf_yaml = Rickle(files, deep=True, load_lambda=True)

        test_conf_yaml.to_yaml_file('./test_out.yaml')

        test_conf_yaml_reload = Rickle('./test_out.yaml', deep=True, load_lambda=True)

        test_conf_yaml_reload.BASICS.outer_math_e()

        obj = test_conf_yaml_reload.TesterClass()
        obj.datenow()
        obj.math_e(99, "^99>")

        os.remove('./test_out.yaml')

        self.assertTrue(True)

    def test_pickle_rick_dict_decon_deserialised_vs_serialised(self):
        test_conf_yaml = Rickle('./tests/placebos/test_config.yaml', deep=True, load_lambda=True)

        d = test_conf_yaml.dict()

        s = test_conf_yaml.to_yaml_string()

        d_ = test_conf_yaml.dict(serialised=True)

        s_ = test_conf_yaml.to_yaml_string(serialised=False)

        self.assertTrue(True)