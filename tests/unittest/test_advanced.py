import unittest
import os
from rickled import BaseRickle, Rickle

class TestAdvanced(unittest.TestCase):

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


