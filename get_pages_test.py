import unittest
import get_pages

class TestGetIndex(unittest.TestCase):
    def test_get_pages_01(self):
        r = get_pages.get_pages([752])
        print(r)


if __name__ == '__main__':
    unittest.main()
