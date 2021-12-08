import unittest
from rickled import ObjectRickler, Rickle

class Testing:

    x = 0.2
    y= 'str'
    z = True
    b = 'asdasd'

    l = [1,2,3,4]
    l_a = [{ 'a' : 7}]

    d = {
        'p' : 0
    }

    def testing_function(self, a, b, c=1):
        print(f'Hello {a}, {b}, and {c}')



class TestObjectRickler(unittest.TestCase):

    def test_rickler(self):

        t = Testing()

        rickler = ObjectRickler()

        d = rickler.deconstruct(t)

        d['testing_function_new'] = {'name' : 'testing_function_new',
                                     'type' : 'function',
                                     # 'includes_self_reference' : True,
                                     'args' : {'a' : None, 'b' : None, 'c' : 1},
                                     'load': """def testing_function_new(a, b, c=1):
    print(f\'{self.__class__.__name__} Howdy {a}, {b}, and {c}\')
"""}

        del d['testing_function']

        y = rickler.to_yaml_string(t)

        r = Rickle(d, deep=True, load_lambda=True)

        # r = rickler.to_rickle(t, deep=True, load_lambda=True)

        # r.testing_function_new('Milly', 'Willy')

        r.x = 99
        r.y = 99
        r.z = 99
        r.b = 99

        obj = rickler.from_rickle(r, Testing)

        obj.testing_function('Jack', 'Sally', 'Justin?')

        obj.testing_function_new('Jack', 'Sally')

        self.assertTrue(True)


