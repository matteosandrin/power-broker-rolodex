import unittest
import get_pages


class TestGetIndex(unittest.TestCase):

    def test_expand_page_nums_2(self):
        r = get_pages.expand_page_nums([20, 28, 29, 30, 32], 2)
        self.assertEqual(r, [18, 19, 20, 21, 22, 26, 27,
                         28, 29, 30, 31, 32, 33, 34])

    def test_expand_page_nums_1(self):
        r = get_pages.expand_page_nums([20, 28, 29, 30, 32], 1)
        self.assertEqual(r, [19, 20, 21, 27, 28, 29, 30, 31, 32, 33])

    def test_expand_page_nums_0(self):
        r = get_pages.expand_page_nums([20, 28, 29, 30, 32], 0)
        self.assertEqual(r, [20, 28, 29, 30, 32])

    def test_page_nums_to_page_ranges_1(self):
        r = get_pages.page_nums_to_page_ranges([20, 28, 29, 30, 32])
        self.assertEqual(r, [(20, 21), (28, 31), (32, 33)])

    def test_page_nums_to_page_ranges_2(self):
        r = get_pages.page_nums_to_page_ranges(
            [18, 19, 20, 21, 22, 26, 27, 28, 29, 30, 31, 32, 33, 34])
        self.assertEqual(r, [(18, 23), (26, 35)])


if __name__ == '__main__':
    unittest.main()
