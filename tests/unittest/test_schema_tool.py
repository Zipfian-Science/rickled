import unittest
import os
from rickled.tools import Schema

class TestAdvanced(unittest.TestCase):

    def test_lists(self):
        schem_d = {
            'type': 'dict',
            'schema': {
                'values_empty': {
                    'type': 'list',
                    'schema': []
                },
                'values_filled': {
                    'type': 'list',
                    'length': -1,
                    'required': True,
                    'schema': [{'type': 'str'}]
                },
                'values_filled_max': {
                    'type': 'list',
                    'length': 1,
                    'schema': [{'type': 'str'}]
                },
                'values_any': {
                    'type': 'list',
                    'schema': [{'type': 'any'}]
                },
                'values_nullable': {
                    'type': 'list',
                    'nullable': True,
                    'schema': [{'type': 'bool'}]
                },
            }
        }

        test_all_good = {
            'values_empty': [1, 2, 3],
            'values_filled': ['a', 'b', 'c'],
            'values_filled_max': ['a']
        }

        test_missing_good = {
            'values_empty': [],
            'values_filled': ['a', 'b', 'c']
        }

        test_missing_fail = {
            'values_empty': [1, 2, 3],
            'values_filled_max': ['a']
        }

        test_type_err = {
            'values_empty': [],
            'values_filled': [1, 2, 3]
        }

        test_type_err_second = {
            'values_empty': [],
            'values_filled': ['a', 'b', 'c', 'd', 1, 'e']
        }

        test_too_long = {
            'values_empty': [1, 2, 3],
            'values_filled': ['a', 'b', 'c'],
            'values_filled_max': ['a', 'b']
        }

        test_mixed = {
            'values_empty': [],
            'values_filled': ['a', 'b', 'c'],
            'values_any': [8, '0.1', True, .99]
        }

        test_nullable_okay = {
            'values_empty': [],
            'values_filled': ['a', 'b', 'c'],
            'values_any': [8, '0.1', True, .99],
            'values_nullable': None
        }

        test_nullable_fail_type = {
            'values_empty': [],
            'values_filled': ['a', 'b', 'c'],
            'values_any': [8, '0.1', True, .99],
            'values_nullable': ['true', 'false']
        }

        test_nullable_fail_null = {
            'values_empty': [],
            'values_filled': ['a', 'b', 'c'],
            'values_any': None,
            'values_nullable': None
        }

        test_empty_null_fail = {
            'values_empty': None,
            'values_filled': ['a', 'b', 'c'],
            'values_filled_max': ['a']
        }

        test_empty_fail_type = {
            'values_empty': 'string',
            'values_filled': ['a', 'b', 'c'],
            'values_filled_max': ['a']
        }

        self.assertTrue(Schema.schema_validation(test_all_good, schem_d))

        self.assertTrue(Schema.schema_validation(test_missing_good, schem_d))

        self.assertFalse(Schema.schema_validation(test_missing_fail, schem_d))

        self.assertFalse(Schema.schema_validation(test_type_err, schem_d))
        self.assertFalse(Schema.schema_validation(test_type_err_second, schem_d))
        self.assertFalse(Schema.schema_validation(test_too_long, schem_d))

        self.assertTrue(Schema.schema_validation(test_mixed, schem_d))
        self.assertTrue(Schema.schema_validation(test_nullable_okay, schem_d))

        self.assertFalse(Schema.schema_validation(test_nullable_fail_type, schem_d))
        self.assertFalse(Schema.schema_validation(test_nullable_fail_null, schem_d))
        self.assertFalse(Schema.schema_validation(test_empty_fail_type, schem_d))
        self.assertFalse(Schema.schema_validation(test_empty_null_fail, schem_d))


    def test_primitives(self):
        schem_d = {
            'type': 'dict',
            'schema': {
                'A': {'type': 'int', 'required': True},
                'a': {'type': 'float'},
                'b': {'type': 'any'},
                'c': {'type': 'bool'},
                'd': {'type': 'str', 'nullable': True},
                'e': {'type': 'str', 'nullable': True, 'required': True}
            }
        }

        test_all_good = {
            'A': 10,
            'a': .90,
            'e': 'string'
        }

        test_missing_good = {
            'A': 10,
            'e': 'string'
        }

        test_missing_fail = {
            'b': 10,
            'c': .90,
            'e': 'string'
        }

        test_type_err = {
            'A': 10,
            'a': 90,
            'e': 'string'
        }

        test_type_any = {
            'A': 10,
            'a': .89,
            'b': .99,
            'e': 'string'
        }

        test_fail_null = {
            'A': None,
            'e': 'string'
        }

        test_fail_okay = {
            'A': 1,
            'd': None,
            'e': 'string'
        }

        test_fail_missing_nullable = {
            'A': 1,
            'd': None,
        }

        test_okay_nullable = {
            'A': 1,
            'd': None,
            'e': None
        }

        test_fail_nullable_type = {
            'A': 1,
            'd': None,
            'e': 1
        }

        self.assertTrue(Schema.schema_validation(test_all_good, schem_d))
        self.assertTrue(Schema.schema_validation(test_missing_good, schem_d))

        self.assertFalse(Schema.schema_validation(test_missing_fail, schem_d))
        self.assertFalse(Schema.schema_validation(test_type_err, schem_d))

        self.assertTrue(Schema.schema_validation(test_type_any, schem_d))

        self.assertFalse(Schema.schema_validation(test_fail_null, schem_d))

        self.assertTrue(Schema.schema_validation(test_fail_okay, schem_d))

        self.assertFalse(Schema.schema_validation(test_fail_missing_nullable, schem_d))
        self.assertTrue(Schema.schema_validation(test_okay_nullable, schem_d))

        self.assertFalse(Schema.schema_validation(test_fail_nullable_type, schem_d))
