import unittest
from rickle.net import serve_rickle_http
from rickle import Rickle

class TestNet(unittest.TestCase):

    def test_basic_auth(self):
        serve_rickle_http(rickle=Rickle({'hello': 'world'}),
                          port=8082,
                          interface='',
                          serialised=False,
                          output_type='JSON',
                          basic_auth={'motha':'sucka'}
                          )

if __name__ == "__main__":
    unittest.main()