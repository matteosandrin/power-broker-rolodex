import unittest
import parse_index

# Boilerplate code for a test case


class TestParseIndex(unittest.TestCase):
    def test_parse_pages_default(self):
        pages_str = "1, 5, 7"
        r = parse_index.parse_pages(pages_str)
        self.assertEqual(r, [
            1, 5, 7
        ])
    
    def test_parse_pages_range_1char(self):
        pages_str = "1, 10-12, 20"
        r = parse_index.parse_pages(pages_str)
        self.assertEqual(r, [
            1, 10, 11, 12, 20
        ])

    def test_parse_pages_range_2char(self):
        pages_str = "1, 119-22, 130"
        r = parse_index.parse_pages(pages_str)
        self.assertEqual(r, [
            1, 119, 120, 121, 122, 130
        ])


if __name__ == '__main__':
    unittest.main()
