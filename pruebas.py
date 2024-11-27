import unittest
from remoteset import RemoteSet
from remotetypes.iterable import Iterable

class TestRemoteSet(unittest.TestCase):
    def setUp(self):
        self.remote_set = RemoteSet()

    def test_add(self):
        self.remote_set.add("item1")
        self.assertIn("item1", self.remote_set.storage)

    def test_remove(self):
        self.remote_set.add("item1")
        self.remote_set.remove("item1")
        self.assertNotIn("item1", self.remote_set.storage)

    def test_contains(self):
        self.remote_set.add("item1")
        self.assertTrue(self.remote_set.contains("item1"))
        self.assertFalse(self.remote_set.contains("item2"))

    def test_length(self):
        self.remote_set.add("item1")
        self.remote_set.add("item2")
        self.assertEqual(self.remote_set.length(), 2)

    def test_hash(self):
        self.remote_set.add("item1")
        self.remote_set.add("item2")
        self.assertIsInstance(self.remote_set.hash(), int)

    def test_iterable(self):
        iterable = Iterable(self.remote_set.storage)
        self.assertEqual(list(iterable), list(self.remote_set.storage))

if __name__ == "__main__":
    unittest.main()