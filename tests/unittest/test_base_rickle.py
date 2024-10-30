import unittest
from rickled import BaseRickle

class TestBasicRickle(unittest.TestCase):

    def setUp(self):
        self.expected_dict = {
            'key_one': 'value_one',
            'key_three': 'value_three',
        }
        self.base_rickle = BaseRickle(self.expected_dict)

    def test_items(self):
        items = list(self.base_rickle.items())
        self.assertListEqual(list(self.expected_dict.items()), items)

    def test_get(self):
        self.assertEqual(self.base_rickle.get("key_one"), "value_one")
        self.assertIsNone(self.base_rickle.get("nonexistent_key"))

    def test_set(self):
        self.base_rickle.set("key_two", "value_two")
        self.assertEqual(self.base_rickle.get("key_two"), "value_two")
        # Updating an existing key
        self.base_rickle.set("key_one", "new_value")
        self.assertEqual(self.base_rickle.get("key_one"), "new_value")

    def test_remove(self):
        self.base_rickle.remove("key_one")
        self.assertIsNone(self.base_rickle.get("key_one"))
        with self.assertRaises(KeyError):
            self.base_rickle.remove("nonexistent_key")

    def test_values(self):
        values = list(self.base_rickle.values())
        self.assertIn("value_one", values)
        self.assertIn("value_three", values)

    def test_keys(self):
        keys = list(self.base_rickle.keys())
        self.assertIn("key_one", keys)
        self.assertIn("key_three", keys)

    def test_dict(self):
        as_dict = self.base_rickle.dict()
        self.assertDictEqual(as_dict, self.expected_dict)

    def test_has(self):
        self.assertTrue(self.base_rickle.has("key_one"))
        self.assertFalse(self.base_rickle.has("nonexistent_key"))

    def test_add(self):
        self.base_rickle.add("new_added", 6.667)
        self.assertEqual(self.base_rickle.new_added, 6.667)
        # Check if it raises an error when adding property that already exists
        with self.assertRaises(NameError):
            self.base_rickle.add("new_added", "new_value")

    def test_meta(self):
        self.base_rickle.add("new_added", 6.667)

        self.assertDictEqual(self.base_rickle.meta("new_added"), {'type': 'attribute', 'value': 6.667})

    def test_item_get(self):
        for key in self.expected_dict.keys():
            self.assertEquals(self.base_rickle[key], self.expected_dict[key])

    def test_item_set(self):
        self.base_rickle['new_key'] = 88

        self.assertEquals(self.base_rickle['new_key'], 88)
        self.assertEquals(self.base_rickle.new_key, 88)

    def test_item_del(self):
        del self.base_rickle['key_one']

        with self.assertRaises(KeyError):
            is_true = self.base_rickle['key_one'] == "value_one"

        with self.assertRaises(AttributeError):
            is_true = self.base_rickle.key_one == "value_one"
    def test_iterator(self):
        expected = {
            'first': {
                'message': 'hello world'
            },
            'second': {
                'message': 'hello world'
            }
        }

        base_rickle = BaseRickle(expected)

        for obj in base_rickle:
            self.assertEquals(obj.message, 'hello world')