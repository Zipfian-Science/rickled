import unittest
import os
from rickled import BaseRickle, Rickle

class TestAdvanced(unittest.TestCase):

    def test_load_lambda_overload(self):
        yaml = """
main:
    file:
        type: from_file
        file_path: './tests/placebos/test_security.yaml'
        load_as_rick: true
        deep: true
        load_lambda: false
        """

        # Unsafe loading
        test_conf_yaml_unsafe = Rickle(yaml, load_lambda=False)

        self.assertTrue(callable(test_conf_yaml_unsafe.main.file.root.link_to_file.bad_function))

        # Set env var and safe load
        os.environ["RICKLE_SAFE_LOAD"] = "1"

        test_conf_yaml_safe = Rickle(yaml, load_lambda=False)

        self.assertIsInstance(test_conf_yaml_safe.main.file.root.link_to_file.bad_function, dict)

        # Still safe due to env
        test_conf_yaml = Rickle('./tests/placebos/test_malicious.yaml', load_lambda=True)

        self.assertIsInstance(test_conf_yaml.bad_function, dict)

        # Set unsafe again
        del os.environ['RICKLE_SAFE_LOAD']

        test_conf_yaml = Rickle('./tests/placebos/test_malicious.yaml', load_lambda=True)

        self.assertTrue(callable(test_conf_yaml.bad_function))

    def test_search_path(self):
        yaml = """
path:
    to:
        second: 1
    and:
        second: 1
    another: 0
route:
    second: 1
        """

        test_rickle = BaseRickle(yaml)

        list_of_paths = test_rickle.search_path(key='second')
        expected = ['/path/to/second', '/path/and/second', '/route/second']

        self.assertIsInstance(list_of_paths, list)
        self.assertListEqual(list_of_paths, expected)

        list_of_paths = test_rickle.search_path(key='third')

        self.assertIsInstance(list_of_paths, list)
        self.assertEqual(len(list_of_paths), 0)

        for path in expected:
            self.assertEqual(test_rickle(path=path), 1)

    def test_path_string(self):

        yaml = """
path:
    datenow:
        type: lambda
        import:
            - "from datetime import datetime as dd"
        load: "dd.utcnow().strftime('%Y-%m-%d')"
    level_one:
        level_two:                    
            member: 42                    
            list_member:
                - 1
                - 0
                - 1 
                - 1
                - 1
        funcs:
            type: function
            name: funcs
            args:
                x: 42
                y: worl
            load: >
                def funcs(x, y):
                    _x = int(x) 
                    return f'Hello {y}, {_x / len(y)}!'
        """

        test_rickle = Rickle(yaml, load_lambda=True)

        v = test_rickle('/path/level_one/level_two/member')

        self.assertEqual(v, 42)

        v = test_rickle('/path/level_one/funcs?x=100&y=world')

        self.assertEqual(v, 'Hello world, 20.0!')

        with self.assertRaises(NameError):
            v = test_rickle('/path/level_two/funcs?x=100&y=world')

        with self.assertRaises(TypeError):
            v = test_rickle('/path/level_one/level_two/member?x=100&y=world')

        with self.assertRaises(TypeError):
            v = test_rickle('/path/level_one/funcs?x=100&z=world')

        v = test_rickle('/path/level_one/funcs?x=100')

        self.assertEqual(v, 'Hello worl, 25.0!')

        v = test_rickle('/path/datenow')

        self.assertIsInstance(v, str)

    def test_self_reference(self):
        y = """
const:
  f: 0.5
get_area:
  type: function
  name: get_area
  is_method: true
  args:
     x: 10
     y: 10
     z: null
  import:
     - math
  load: >
     def get_area(self, x, y, z):
        if not z is None:
           area = (x * y) + (x * z) + (y * z)
           area = 2 * area
        else:
           area = x * y
        return math.floor(area * self.const.f)
        """

        r = Rickle(y, load_lambda=True)

        area = r.get_area(x=10, y=10, z=10)

        self.assertEqual(area, 300)

        y = """
        const:
            f: 0.5
        functions:
            get_area:
              type: function
              name: get_area
              is_method: true
              args:
                 x: 10
                 y: 10
                 z: null
              import:
                 - math
              load: >
                 def get_area(self, x, y, z):
                    if not z is None:
                       area = (x * y) + (x * z) + (y * z)
                       area = 2 * area
                    else:
                       area = x * y
                    return math.floor(area * self.const.f)
                """

        r = Rickle(y, load_lambda=True)

        with self.assertRaises(AttributeError):
            area = r.functions.get_area(x=10, y=10, z=10)

    def test_hot_load_api(self):

        s = """
crypt_exchanges:
  type: api_json
  url: https://cryptingup.com/api/exchanges
  expected_http_status: 200
  load_as_rick: true
  deep: true
  hot_load: true
        """

        r = Rickle(s)

        observed = r.crypt_exchanges()

        self.assertTrue(isinstance(observed, Rickle))

        s = """
crypt_exchanges:
  type: api_json
  url: https://cryptingup.com/api/exchanges
  expected_http_status: 200
  load_as_rick: true
  deep: true
        """

        r = Rickle(s)

        self.assertTrue(isinstance(r.crypt_exchanges, Rickle))