import unittest
import pages
import json


class TestGetIndex(unittest.TestCase):

    def test_expand_page_nums_2(self):
        r = pages.expand_page_nums([20, 28, 29, 30, 32], 2)
        self.assertEqual(r, [18, 19, 20, 21, 22, 26, 27,
                         28, 29, 30, 31, 32, 33, 34])

    def test_expand_page_nums_1(self):
        r = pages.expand_page_nums([20, 28, 29, 30, 32], 1)
        self.assertEqual(r, [19, 20, 21, 27, 28, 29, 30, 31, 32, 33])

    def test_expand_page_nums_0(self):
        r = pages.expand_page_nums([20, 28, 29, 30, 32], 0)
        self.assertEqual(r, [20, 28, 29, 30, 32])

    def test_page_nums_to_page_ranges_1(self):
        r = pages.page_nums_to_page_ranges([20, 28, 29, 30, 32])
        self.assertEqual(r, [(20, 21), (28, 31), (32, 33)])

    def test_page_nums_to_page_ranges_2(self):
        r = pages.page_nums_to_page_ranges(
            [18, 19, 20, 21, 22, 26, 27, 28, 29, 30, 31, 32, 33, 34])
        self.assertEqual(r, [(18, 23), (26, 35)])

    def test_find_chapter_location(self):
        metadata_file = open("./power-broker-metadata.json")
        METADATA = json.load(metadata_file)

        last_loc = -1
        for c in METADATA["chapters"]:
            loc = pages.find_chapter_location(c)
            self.assertNotEqual(loc, -1)
            self.assertTrue(last_loc < loc)
            last_loc = loc

        metadata_file.close()


if __name__ == '__main__':
    unittest.main()
